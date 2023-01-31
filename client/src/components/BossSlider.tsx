import * as Slider from "@radix-ui/react-slider";
import styles from "/styles/components/modules/BossSlider.module.scss";

/**
 *
 * @function BossSlider
 * @param {Object} value
 * @param {function} onValueChange
 *
 * @returns {JSX.Element} Returns a slider to choose a level from 1-5
 */
export const BossSlider = ({ value, onValueChange }: any) => {
  return (
    <div className={styles.slider_container}>
      <div className={styles.value_container}>
        <div className={styles.slider_label}>Level:</div>
        <div className={styles.slider_value}>{value}</div>
      </div>
      <Slider.Root
        className={styles.boss_slider}
        defaultValue={[3]}
        min={1}
        max={5}
        step={1}
        aria-label="Level"
        onValueChange={onValueChange}
      >
        <Slider.Track className={styles.boss_slider_track}>
          <Slider.Range className={styles.boss_slider_range} />
        </Slider.Track>
        <Slider.Thumb className={styles.boss_slider_thumb} />
      </Slider.Root>
    </div>
  );
};
