import { useDraggable } from "@dnd-kit/core";
import { format, isBefore, startOfToday } from "date-fns";
import { Building2, Calendar, AlertCircle } from "lucide-react";
import type { Application } from "../../types";
import { StatusBadge } from "../ui/Badge";
import { cn } from "../../utils/cn";

interface ApplicationCardProps {
  application: Application;
  onClick?: (app: Application) => void;
  isOverlay?: boolean;
}

export function ApplicationCard({
  application,
  onClick,
  isOverlay,
}: ApplicationCardProps) {
  const { attributes, listeners, setNodeRef, transform, isDragging } =
    useDraggable({
      id: application.id,
      data: {
        type: "Application",
        application,
      },
    });

  const style = transform
    ? {
        transform: `translate3d(${transform.x}px, ${transform.y}px, 0)`,
      }
    : undefined;

  const isOverdue =
    application.follow_up_date &&
    isBefore(new Date(application.follow_up_date), startOfToday());
  const interviewCount = application.interviews?.length || 0;

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={cn(
        "group relative flex cursor-grab flex-col gap-3 rounded-lg border border-gray-200 bg-white p-4 text-left shadow-sm transition-all hover:border-indigo-300 hover:shadow-md active:cursor-grabbing",
        isDragging && !isOverlay ? "opacity-50" : "opacity-100",
        isOverlay ? "rotate-2 scale-105 shadow-xl cursor-grabbing" : "",
      )}
      onClick={() => onClick?.(application)}
      {...attributes}
      {...listeners}
    >
      <div className="flex items-start justify-between gap-2">
        <div>
          <h4 className="font-semibold text-gray-900 line-clamp-1">
            {application.company_name}
          </h4>
          <p className="text-sm text-gray-600 line-clamp-1">
            {application.role_title}
          </p>
        </div>
        <StatusBadge
          status={application.priority === "high" ? "warning" : "default"}
        />
      </div>

      <div className="mt-1 flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-gray-500">
        <div className="flex items-center gap-1">
          <Calendar className="h-3.5 w-3.5" />
          <span>
            {application.applied_date
              ? format(new Date(application.applied_date), "MMM d, yyyy")
              : "No date"}
          </span>
        </div>

        {interviewCount > 0 && (
          <div className="flex items-center gap-1 font-medium text-indigo-600">
            <Building2 className="h-3.5 w-3.5" />
            <span>
              {interviewCount}{" "}
              {interviewCount === 1 ? "Interview" : "Interviews"}
            </span>
          </div>
        )}

        {isOverdue && (
          <div className="flex items-center gap-1 font-medium text-red-600">
            <AlertCircle className="h-3.5 w-3.5" />
            <span>Overdue follow-up</span>
          </div>
        )}
      </div>
    </div>
  );
}
