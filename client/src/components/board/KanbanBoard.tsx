import { useState, useMemo } from "react";
import {
  DndContext,
  DragOverlay,
  useSensor,
  useSensors,
  PointerSensor,
  closestCorners,
} from "@dnd-kit/core";
import type { DragStartEvent, DragEndEvent } from "@dnd-kit/core";
import { KanbanColumn } from "./KanbanColumn";
import { ApplicationCard } from "./ApplicationCard";
import { ApplicationDrawer } from "../application/ApplicationDrawer";
import {
  useApplications,
  useUpdateApplicationStatus,
} from "../../hooks/useApplications";
import type { Application, ApplicationStatus } from "../../types";

const COLUMNS: { id: ApplicationStatus; title: string }[] = [
  { id: "wishlist", title: "Wishlist" },
  { id: "applied", title: "Applied" },
  { id: "phone_screen", title: "Phone Screen" },
  { id: "interview", title: "Interview" },
  { id: "offer", title: "Offer" },
  { id: "rejected", title: "Rejected" },
  { id: "closed", title: "Closed" },
];

interface KanbanBoardProps {
  filters: {
    search: string;
    priority: string;
  };
}

export function KanbanBoard({ filters }: KanbanBoardProps) {
  // Pass filters to useApplications to refetch nicely matching filtering
  const queryParams: Record<string, string> = {};
  if (filters.search) queryParams.search = filters.search;
  if (filters.priority) queryParams.priority = filters.priority;

  const { data, isLoading } = useApplications(queryParams);
  const { mutate: updateStatus } = useUpdateApplicationStatus();

  const [activeApplication, setActiveApplication] =
    useState<Application | null>(null);

  // Drawer state
  const [selectedApplication, setSelectedApplication] =
    useState<Application | null>(null);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 5,
      },
    }),
  );

  const applications = useMemo(() => data?.results || [], [data]);

  const onDragStart = (event: DragStartEvent) => {
    const { active } = event;
    const application = active.data.current?.application as
      | Application
      | undefined;
    if (application) {
      setActiveApplication(application);
    }
  };

  const onDragEnd = (event: DragEndEvent) => {
    setActiveApplication(null);
    const { active, over } = event;

    if (!over) return;

    const applicationId = active.id as string;
    const fromStatus = active.data.current?.application
      ?.status as ApplicationStatus;
    const toStatus = over.id as ApplicationStatus;

    if (fromStatus && toStatus && fromStatus !== toStatus) {
      updateStatus({ id: applicationId, status: toStatus });
    }
  };

  const handleCardClick = (app: Application) => {
    setSelectedApplication(app);
    setIsDrawerOpen(true);
  };

  if (isLoading) {
    return (
      <div className="flex h-full items-center justify-center bg-gray-50">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-600 border-t-transparent"></div>
      </div>
    );
  }

  return (
    <>
      <div className="flex h-full w-full inset-0 overflow-x-auto overflow-y-hidden p-6 bg-gray-50">
        <DndContext
          sensors={sensors}
          collisionDetection={closestCorners}
          onDragStart={onDragStart}
          onDragEnd={onDragEnd}
        >
          <div className="flex h-full min-h-[500px] gap-6">
            {COLUMNS.map((col) => (
              <KanbanColumn
                key={col.id}
                status={col.id}
                title={col.title}
                applications={applications.filter(
                  (app: Application) => app.status === col.id,
                )}
                onCardClick={handleCardClick}
              />
            ))}
          </div>

          <DragOverlay>
            {activeApplication ? (
              <ApplicationCard application={activeApplication} isOverlay />
            ) : null}
          </DragOverlay>
        </DndContext>
      </div>

      <ApplicationDrawer
        application={selectedApplication}
        isOpen={isDrawerOpen}
        onClose={() => setIsDrawerOpen(false)}
      />
    </>
  );
}
