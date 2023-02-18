import { useEffect, useState } from "react";
import "vite/modulepreload-polyfill";
import { useNavigate, useParams } from "react-router-dom";
import parse, { domToReact } from "html-react-parser";
import { useRef } from "react";
import BossNav from "../components/BossNav";
import { AISubSection } from "../components/AISubSection";
import { AIOverview } from "../components/AIOverview";
import axios from "axios";

/**
 * @function Page
 * Page containing custom wikipedia page, populated with AI components.
 *
 * @returns {JSX.Element} - Returns a JSX element containing the page data.
 */
function Page() {
  const params = useParams();
  const [data, setData] = useState<string | null>(null);
  const [level, setLevel] = useState<number>(3);
  const title = useRef("");
  const initialized = useRef(false);
  const navigate = useNavigate();

  const updateLevel = (level: number[]) => setLevel(level[0]);

  /**
   * fetchContent
   *
   * @async
   * @returns {Promise<void>} - Fetches the content of the page.
   */
  async function fetchContent() {
    await axios({
      method: "get",
      url: `${import.meta.env.VITE_API_URL}/api/wiki/${params.title}`,
    })
      .then(function (response) {
        const data = response!.data;
        setData(data);
      })
      .catch(function (error) {
        console.log(error);
        console.log(error.response.status);
        if (error.response.status == 429) {
          navigate(`/limiting`);
        }
      });
  }

  useEffect(() => {
    if (!initialized.current) {
      initialized.current = true;
      fetchContent();
    }
  }, [level, params.title]);

  useEffect(() => {
    if (!initialized.current) {
      initialized.current = true;
      fetchContent();
    }
  }, [level, params.title]);

  let options = {
    replace: ({ attribs, children }: any) => {
      if (!attribs) {
        return;
      }

      if (attribs.class === "title") {
        title.current = children[0].data;
        title.current = title.current.replaceAll("\n", "");
        return <></>;
      }

      if (attribs.class === "ai_overview") {
        return (
          <AIOverview page_level={level} title={params.title}>
            {domToReact(children, options)}
          </AIOverview>
        );
      }

      if (attribs.class === "ai_sub_section") {
        return (
          <AISubSection page_level={level} title={params.title} id={attribs.id}>
            {domToReact(children, options)}
          </AISubSection>
        );
      }
    },
  };

  return (
    <>
      <BossNav
        title={title.current}
        level={level}
        onLevelChange={updateLevel}
      />

      <div className="content">{parse(data != null ? data : "", options)}</div>
    </>
  );
}

export default Page;
