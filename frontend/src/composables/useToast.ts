import { h, render } from "vue";
import Toast from "@/components/ui/Toast.vue";

export const useToast = () => {
  const showToast = (message: string, type = "default", duration = 3000) => {
    const container = document.createElement("div");
    document.body.appendChild(container);
    const vnode = h(Toast, { message, type, duration });
    render(vnode, container);
    setTimeout(() => {
      render(null, container);
      document.body.removeChild(container);
    }, duration + 500);
  };

  return {
    toast: {
      success: (msg: string, opts = { duration: 3000 }) =>
        showToast(msg, "success", opts.duration || 3000),
      error: (msg: string, opts = { duration: 3000 }) =>
        showToast(msg, "error", opts.duration || 3000),
      warning: (msg: string, opts = { duration: 3000 }) =>
        showToast(msg, "warning", opts.duration || 3000),
      info: (msg: string, opts = { duration: 3000 }) =>
        showToast(msg, "info", opts.duration || 3000),
    },
  };
};
