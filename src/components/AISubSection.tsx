import { useEffect, useRef, useState } from "react";
import { SectionDropdown } from "./SectionDropdown";
import styles from "/styles/components/modules/AISubSection.module.scss";

export const AISubSection = ({ id, title, children, page_level }: any) => {
  const fetched = useRef(0);
  const [level, setLevel] = useState<number>(page_level);

  const [content, setContent] = useState<string>(children);
  const [model, setModel] = useState<string>("");
  const [timestamp, setTimestamp] = useState<string>("");

  useEffect(() => {
    if (fetched.current != level) {
      fetched.current = level;
      fetchContent();
    }
  }, [level]);

  useEffect(() => {
    setLevel(page_level);
  }, [page_level]);

  async function fetchContent() {
    const body = {
      level: level,
      title: title,
      content_id: id,
    };
    console.log(JSON.stringify(body));
    await fetch("/api/wiki/content", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "true",
      },
      body: JSON.stringify(body),
    }).then(async (res) => {
      console.log(res);
      const data = await res.json();
      if (data.content != undefined) {
        setContent(data.content);
        setModel(data.model);
        setTimestamp(data.timestamp);
      }
    });
  }

  const updateLevel = (level: number[]) => {
    console.log("changing level");
    setLevel(level[0]);
  };

  return (
    <div id={id} className={styles.ai_sub_section}>
      <SectionDropdown
        value={level}
        model={model}
        timestamp={timestamp}
        onValueChange={updateLevel}
      />
      <p className={styles.ai_sub_section_content}>{content}</p>
    </div>
  );
};
