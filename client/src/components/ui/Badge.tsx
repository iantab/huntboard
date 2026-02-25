import { cn } from "../../utils/cn";

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "success" | "warning" | "error" | "info";
  children: React.ReactNode;
}

export function Badge({
  className,
  variant = "default",
  children,
  ...props
}: BadgeProps) {
  const variants = {
    default: "bg-gray-100 text-gray-800 border-gray-200",
    info: "bg-blue-100 text-blue-800 border-blue-200",
    success: "bg-green-100 text-green-800 border-green-200",
    warning: "bg-yellow-100 text-yellow-800 border-yellow-200",
    error: "bg-red-100 text-red-800 border-red-200",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold shadow-sm",
        variants[variant],
        className,
      )}
      {...props}
    >
      {children}
    </span>
  );
}

// Helper specific to HuntBoard Application statuses and priorities
export function StatusBadge({ status }: { status: string }) {
  const statusMap: Record<
    string,
    { label: string; variant: BadgeProps["variant"] }
  > = {
    wishlist: { label: "Wishlist", variant: "default" },
    applied: { label: "Applied", variant: "info" },
    phone_screen: { label: "Phone", variant: "info" },
    interview: { label: "Interview", variant: "warning" },
    offer: { label: "Offer", variant: "success" },
    rejected: { label: "Rejected", variant: "error" },
    closed: { label: "Closed", variant: "default" },
  };

  const { label, variant } = statusMap[status] || {
    label: status,
    variant: "default",
  };

  return <Badge variant={variant}>{label}</Badge>;
}
