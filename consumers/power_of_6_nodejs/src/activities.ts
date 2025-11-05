
export async function powerOf6(a: number): Promise<number> {
  const wait_timeout = Number(process.env.ACTIVITY_3_WAIT_TIMEOUT) || 5;
  await new Promise(resolve => setTimeout(resolve, wait_timeout * 1000));
  const result = Math.pow(a, 6);
  return result;
}