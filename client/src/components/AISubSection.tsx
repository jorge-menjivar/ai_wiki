import { useEffect, useRef, useState } from "react";
import { SectionDropdown } from "./SectionDropdown";
import styles from "/styles/components/modules/AISubSection.module.scss";
import axios from "axios";
import { useNavigate } from "react-router-dom";

/**
 * AISubSection Component
 * @component
 *
 * @param {number} id - The id of the content
 * @param {string} title - The title of the content
 * @param {string} children - The content of the section
 * @param {number} page_level - The page level
 *
 * @returns {JSX.Element} Returns a JSX.Element
 */
export const AISubSection = ({ id, title, children, page_level }: any) => {
  const fetched = useRef(0);
  const [level, setLevel] = useState<number>(page_level);

  const [content, setContent] = useState<string>(children);
  const [model, setModel] = useState<string>("");
  const [timestamp, setTimestamp] = useState<string>("");
  const navigate = useNavigate();

  useEffect(() => {
    if (fetched.current != level) {
      fetched.current = level;
      fetchContent();
    }
  }, [level]);

  useEffect(() => {
    setLevel(page_level);
  }, [page_level]);

  /**
   * @async
   * @function fetchContent
   * @description A function that fetches content from the API
   *
   * @param {number} level - The level of the content
   * @param {string} title - The title of the content
   *
   * @returns {Promise<Object>} The response from the API
   */
  async function fetchContent() {
    const body = {
      level: level,
      title: title,
      content_id: id,
    };

    await axios({
      method: "post",
      url: `${import.meta.env.VITE_API_URL}/api/resources/content`,
      data: body,
    })
      .then(function (response) {
        const data = response!.data;
        if (data.content != undefined) {
          setContent(data.content);
          setModel(data.model);
          setTimestamp(data.timestamp);
        }
      })
      .catch(function (error) {
        console.log(error);
        if (error.response.status == 429) {
          navigate(`/limiting`);
        }
      });
  }
  /**
   * Updates the level
   * @param {number[]} level - An array of numbers representing the level
   */
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
