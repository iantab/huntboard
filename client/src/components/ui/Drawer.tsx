import { useEffect } from "react";
import { createPortal } from "react-dom";
import { X } from "lucide-react";
import { Button } from "./Button";
import { cn } from "../../utils/cn";

interface DrawerProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  className?: string;
}

export function Drawer({
  isOpen,
  onClose,
  title,
  children,
  className,
}: DrawerProps) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return createPortal(
    <div className="fixed inset-0 z-50 overflow-hidden">
      <div
        className="absolute inset-0 backdrop-blur-sm bg-black/20 transition-opacity"
        onClick={onClose}
      />
      <div className="pointer-events-none fixed inset-y-0 right-0 flex max-w-full pl-10">
        <div
          className={cn(
            "pointer-events-auto w-screen max-w-md transform transition-transform duration-300 ease-in-out bg-white shadow-xl",
            className,
          )}
        >
          <div className="flex h-full flex-col overflow-y-scroll">
            <div className="px-4 py-6 sm:px-6 flex items-center justify-between border-b border-gray-200">
              {title && (
                <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
              )}
              <Button
                variant="ghost"
                size="sm"
                onClick={onClose}
                className="px-2"
                aria-label="Close panel"
              >
                <X className="h-5 w-5" />
              </Button>
            </div>
            <div className="relative flex-1 px-4 py-6 sm:px-6">{children}</div>
          </div>
        </div>
      </div>
    </div>,
    document.body,
  );
}
