import { forwardRef, LegacyRef, Ref } from "react";
import styles from "/styles/common/BossNav.module.scss";

const myBossNavButton = (
  { src, children, ...props }: any,
  ref: LegacyRef<HTMLButtonElement> | undefined
) => (
  <button ref={ref} className={styles.nav_bar_button} {...props}>
    {children}
  </button>
);
export const BossNavButton = forwardRef(myBossNavButton);

const myStyledImageButton = (
  { src, ...props }: any,
  ref: LegacyRef<HTMLImageElement> | undefined
) => <img src={src} {...props}></img>;
const StyledImageButton = forwardRef(myStyledImageButton);

const myBossNavImageButton = (
  { src, ...props }: any,
  ref: Ref<HTMLImageElement> | undefined
) => (
  <button className={styles.nav_bar_button}>
    <StyledImageButton
      ref={ref}
      src={src}
      className={styles.image_button_img}
      {...props}
    />
  </button>
);
export const BossNavImageButton = forwardRef(myBossNavImageButton);

const myBossNavLogo = (
  { src, ...props }: any,
  ref: Ref<HTMLImageElement> | undefined
) => (
  <StyledImageButton
    ref={ref}
    src={src}
    className={styles.logo_img}
    {...props}
  />
);
export const BossNavLogo = forwardRef(myBossNavLogo);
