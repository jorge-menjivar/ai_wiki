import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import styles from "/styles/components/modules/SectionDropdown.module.scss";
import { SectionSlider } from "./SectionSlider";

/**
 * @function SectionDropdown
 * @description Renders a dropdown menu with a section slider, a model label, and a timestamp label
 * @param {any} value - The current value of the slider
 * @param {any} model - The model of the slider
 * @param {any} timestamp - The timestamp of the slider
 * @param {any} onValueChange - The function to call when the value changes
 */
export const SectionDropdown = ({
  value,
  model,
  timestamp,
  onValueChange,
}: any) => {
  return (
    <DropdownMenu.Root modal={false}>
      <DropdownMenu.Trigger asChild>
        <button className={styles.icon_button} aria-label="Change Level">
          <div className={styles.level}>{value}</div>
        </button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content className={styles.menu_content} sideOffset={5}>
          <DropdownMenu.Item className={styles.menu_item}>
            <SectionSlider value={value} onValueChange={onValueChange} />
          </DropdownMenu.Item>
          <DropdownMenu.Item className={styles.menu_item}>
            <DropdownMenu.Label className={styles.disclaimer}>
              {model}
            </DropdownMenu.Label>
          </DropdownMenu.Item>
          <DropdownMenu.Item className={styles.menu_item}>
            <DropdownMenu.Label className={styles.disclaimer}>
              {timestamp}
            </DropdownMenu.Label>
          </DropdownMenu.Item>

          <DropdownMenu.Arrow className={styles.menu_arrow} />
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
};
