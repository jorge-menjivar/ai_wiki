import { useEffect, useState } from "react";
import "vite/modulepreload-polyfill";
import { useParams } from "react-router-dom";

function Page() {
  const [content, setContent] = useState("");
  const params = useParams();

  useEffect(() => {
    fetch(`/api/wiki/${params.level}/${params.title}`).then(async (res) =>
      setContent(await res.text())
    );
  }, []);

  return (
    <div
      className="content"
      dangerouslySetInnerHTML={{ __html: content }}
    ></div>
  );
}

export default Page;
