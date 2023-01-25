import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import {
  HamburgerMenuIcon,
  DotFilledIcon,
  CheckIcon,
  ChevronRightIcon,
} from "@radix-ui/react-icons";
import styles from "/styles/components/modules/SectionDropdown.module.scss";
import React from "react";
import { SectionSlider } from "./SectionSlider";

export const SectionDropdown = ({
  value,
  model,
  timestamp,
  onValueChange,
}: any) => {
  return (
    <DropdownMenu.Root>
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
