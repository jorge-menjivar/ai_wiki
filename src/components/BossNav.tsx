import { useEffect, useMemo, useRef, useState } from "react";
import { debounce } from "../lib/Helpers";
import { BossSlider } from "./BossSlider";
import styles from "/styles/components/modules/BossNav.module.scss";

const BossNavRoot = ({ children, show }: any) => {
  return (
    <div style={{ top: show ? "-1px" : "-70px" }} className={styles.boss_nav}>
      {children}
    </div>
  );
};

const BossNavColumns = ({ children }: any) => {
  return <div className={styles.boss_nav_list}>{children}</div>;
};

const BossNavLeft = ({ children, to, theme, src, ...props }: any) => {
  return <div className={styles.boss_nav_left}>{children}</div>;
};

const BossNavCenter = ({ children }: any) => {
  return <div className={styles.boss_nav_center}>{children}</div>;
};

const BossNavRight = ({ children }: any) => {
  return <div className={styles.boss_nav_right}>{children}</div>;
};

const BossNavItem = ({ children }: any) => {
  return <div className={styles.boss_nav_item}>{children}</div>;
};

function BossNav({ children, title, level, onLevelChange }: any) {
  const prevLoc = useRef(0);
  const [show, setShow] = useState(true);

  const handleScroll = () => {
    // Only hiding in devices with width less than 900px.
    if (window.innerWidth < 900) {
      const currLoc = window.pageYOffset;
      if (Math.abs(prevLoc.current - currLoc) > 60 || currLoc < 10) {
        setShow(prevLoc.current > currLoc || currLoc < 10);
        prevLoc.current = currLoc;
      }
    } else {
      setShow(true);
    }
  };

  const debouncedScroll = useMemo(() => {
    return debounce(handleScroll, 15);
  }, []);

  useEffect(() => {
    window.addEventListener("scroll", debouncedScroll);
    return () => window.removeEventListener("scroll", debouncedScroll);
  }, []);

  return (
    <BossNavRoot show={show}>
      <BossNavColumns>
        <BossNavLeft>
          <BossNavItem>
            <div className={styles.boss_nav_title}>{title}</div>
            {/* <a href="/" className={styles.boss_nav_link}>
              <div className={styles.boss_nav_title}>{title}</div>
            </a> */}
          </BossNavItem>
        </BossNavLeft>
        <BossNavCenter>
          <BossSlider value={level} onValueChange={onLevelChange} />
        </BossNavCenter>
        <BossNavRight>
          <BossNavItem>
            <a href="/" className={styles.boss_nav_link}>
              <div className={styles.boss_nav_title}>Readuce</div>
            </a>
          </BossNavItem>
        </BossNavRight>
      </BossNavColumns>
    </BossNavRoot>
  );
}

export default BossNav;
