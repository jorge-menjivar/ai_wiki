import { useEffect, useState } from "react";
import "vite/modulepreload-polyfill";
import { useParams } from "react-router-dom";
import parse, { domToReact } from "html-react-parser";
import { useRef } from "react";
import BossNav from "../components/BossNav";
import { AISubSection } from "../components/AISubSection";
import { AIOverview } from "../components/AIOverview";

function Page() {
  const params = useParams();
  const [data, setData] = useState<string | null>(null);
  const [level, setLevel] = useState<number>(3);
  const title = useRef("");
  const fetched = useRef(0);

  const updateLevel = (level: number) => setLevel(level);

  async function fetchContent() {
    try {
      const res = await fetch(`/api/wiki/${level}/${params.title}`);
      const data = await res.text();
      setData(data);
      // console.log(data);
    } catch (error: any) {
      if (error.name !== "AbortError") {
        // TODO
        // Non-aborted error handling goes here
      }
    }
  }

  useEffect(() => {
    if (fetched.current != level) {
      console.log("fetching");
      fetched.current = level;
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
        title.current = title.current.replaceAll(" ", "");
        return <></>;
      }

      if (attribs.class === "ai_overview") {
        return <AIOverview id={attribs.id}>{children}</AIOverview>;
      }

      if (attribs.class === "ai_sub_section") {
        return (
          <AISubSection
            original_level={level}
            title={params.title}
            id={attribs.id}
          >
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
