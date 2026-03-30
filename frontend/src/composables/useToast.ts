import { useToast as usePrimeToast } from "primevue/usetoast";

const severityMap: Record<string, string> = {
  success: "success",
  error: "error",
  warning: "warn",
  info: "info",
  default: "secondary",
};

export const useToast = () => {
  const primeToast = usePrimeToast();

  const showToast = (message: string, type = "default", duration = 3000) => {
    primeToast.add({
      severity: severityMap[type] ?? "secondary",
      detail: message,
      life: duration,
    });
  };

  return {
    toast: {
      success: (msg: string, opts = { duration: 3000 }) =>
        showToast(msg, "success", opts.duration ?? 3000),
      error: (msg: string, opts = { duration: 3000 }) =>
        showToast(msg, "error", opts.duration ?? 3000),
      warning: (msg: string, opts = { duration: 3000 }) =>
        showToast(msg, "warning", opts.duration ?? 3000),
      info: (msg: string, opts = { duration: 3000 }) =>
        showToast(msg, "info", opts.duration ?? 3000),
    },
  };
};