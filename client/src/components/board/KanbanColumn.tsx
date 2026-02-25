import { useDroppable } from "@dnd-kit/core";
import { ApplicationCard } from "./ApplicationCard";
import type { Application, ApplicationStatus } from "../../types";

interface KanbanColumnProps {
  status: ApplicationStatus;
  title: string;
  applications: Application[];
  onCardClick?: (app: Application) => void;
  onAddClick?: (status: ApplicationStatus) => void;
}

export function KanbanColumn({
  status,
  title,
  applications,
  onCardClick,
  onAddClick,
}: KanbanColumnProps) {
  const { setNodeRef, isOver } = useDroppable({
    id: status,
    data: {
      type: "Column",
      status,
    },
  });

  return (
    <div className="flex h-full w-80 shrink-0 flex-col rounded-xl bg-gray-50/50">
      <div className="flex items-center justify-between p-4 pb-2">
        <div className="flex items-center gap-2">
          <h3 className="font-semibold text-gray-900">{title}</h3>
          <span className="flex h-5 items-center justify-center rounded-full bg-gray-200 px-2 text-xs font-medium text-gray-600">
            {applications.length}
          </span>
        </div>
        {onAddClick && (
          <button
            onClick={() => onAddClick(status)}
            className="flex h-6 w-6 items-center justify-center rounded-md text-gray-400 hover:bg-gray-200 hover:text-gray-900"
            aria-label={`Add application to ${title}`}
          >
            +
          </button>
        )}
      </div>

      <div
        ref={setNodeRef}
        className={`flex flex-1 flex-col gap-3 overflow-y-auto p-4 transition-colors ${
          isOver ? "bg-indigo-50/50" : ""
        }`}
      >
        {applications.map((app) => (
          <ApplicationCard
            key={app.id}
            application={app}
            onClick={onCardClick}
          />
        ))}
        {applications.length === 0 && (
          <div className="flex h-24 items-center justify-center rounded-lg border-2 border-dashed border-gray-200 bg-transparent text-sm text-gray-400">
            Drop here
          </div>
        )}
      </div>
    </div>
  );
}
