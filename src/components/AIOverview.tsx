import { domToReact } from "html-react-parser";
import { useState } from "react";
import styles from "/styles/components/modules/AIOverview.module.scss";

export const AIOverview = ({ children, level }: any) => {
  let options = {
    replace: ({ attribs, children }: any) => {
      if (!attribs) {
        return;
      }

      if (attribs.class === "overview_disclaimer") {
        return (
          <p className={styles.overview_disclaimer}>
            {domToReact(children, options)}
          </p>
        );
      }

      if (attribs.class === "overview_content") {
        return (
          <p className={styles.overview_content}>
            {domToReact(children, options)}
          </p>
        );
      }
    },
  };

  return (
    <div className={styles.ai_overview}>{domToReact(children, options)}</div>
  );
};
