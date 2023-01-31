/**
 * Creates a debounced function that delays invoking `func` until after `waitFor` milliseconds have elapsed since the last time the debounced function was invoked.
 *
 * @param {Function} func - The function to debounce.
 * @param {number} waitFor - The number of milliseconds to delay.
 *
 * @returns {Function} - Returns the new debounced function.
 */
export const debounce = <F extends (...args: Parameters<F>) => ReturnType<F>>(
  func: F,
  waitFor: number
) => {
  let timeout: NodeJS.Timeout;

  const debounced = (...args: Parameters<F>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), waitFor);
  };

  return debounced;
};
