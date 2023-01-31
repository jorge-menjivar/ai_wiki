import * as Slider from "@radix-ui/react-slider";
import styles from "/styles/components/modules/SectionSlider.module.scss";

/**
 *
 * @function SectionSlider
 * @param {Object} value
 * @param {function} onValueChange
 *
 * @returns {JSX.Element} Returns a slider to choose a level from 1-5
 */
export const SectionSlider = ({ value, onValueChange }: any) => {
  return (
    <Slider.Root
      className={styles.slider}
      defaultValue={[value]}
      min={1}
      max={5}
      step={1}
      aria-label="Level"
      onValueChange={onValueChange}
    >
      <Slider.Track className={styles.slider_track}>
        <Slider.Range className={styles.slider_range} />
      </Slider.Track>
      <Slider.Thumb className={styles.slider_thumb} />
    </Slider.Root>
  );
};
