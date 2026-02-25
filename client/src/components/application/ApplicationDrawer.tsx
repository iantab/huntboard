import { Drawer } from "../ui/Drawer";
import { Textarea } from "../ui/Textarea";
import { StatusBadge } from "../ui/Badge";
import { useUpdateApplication } from "../../hooks/useApplications";
import type { Application } from "../../types";

interface ApplicationDrawerProps {
  application: Application | null;
  isOpen: boolean;
  onClose: () => void;
}

export function ApplicationDrawer({
  application,
  isOpen,
  onClose,
}: ApplicationDrawerProps) {
  const { mutate: updateApplication } = useUpdateApplication();

  if (!application) return null;

  const handleBlur = <K extends keyof Application>(
    field: K,
    value: Application[K],
  ) => {
    if (application[field] !== value) {
      updateApplication({ id: application.id, data: { [field]: value } });
    }
  };

  return (
    <Drawer isOpen={isOpen} onClose={onClose} className="w-full max-w-2xl">
      <div className="space-y-6">
        {/* Header section with inline edits */}
        <div className="flex flex-col gap-4 border-b border-gray-100 pb-6">
          <div className="flex items-start justify-between">
            <div className="flex-1 space-y-2">
              <input
                className="w-full bg-transparent text-2xl font-bold text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 rounded px-1 -ml-1 transition-colors hover:bg-gray-50"
                defaultValue={application.company_name}
                onBlur={(e) => handleBlur("company_name", e.target.value)}
                placeholder="Company Name"
              />
              <input
                className="w-full bg-transparent text-lg text-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 rounded px-1 -ml-1 transition-colors hover:bg-gray-50"
                defaultValue={application.role_title}
                onBlur={(e) => handleBlur("role_title", e.target.value)}
                placeholder="Role Title"
              />
            </div>
            <StatusBadge status={application.status} />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-medium text-gray-500">
                Location
              </label>
              <input
                className="w-full bg-transparent text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 rounded px-1 -ml-1 hover:bg-gray-50"
                defaultValue={application.location || ""}
                onBlur={(e) => handleBlur("location", e.target.value)}
                placeholder="e.g. Remote, Tokyo"
              />
            </div>
            <div>
              <label className="text-xs font-medium text-gray-500">
                Job URL
              </label>
              <input
                className="w-full bg-transparent text-sm text-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 rounded px-1 -ml-1 hover:bg-gray-50"
                defaultValue={application.job_url || ""}
                onBlur={(e) => handleBlur("job_url", e.target.value)}
                placeholder="https://..."
              />
            </div>
          </div>
        </div>

        {/* Notes Editor */}
        <div>
          <h3 className="text-sm font-medium text-gray-900 mb-2">Notes</h3>
          <Textarea
            defaultValue={application.notes}
            onBlur={(e) => handleBlur("notes", e.target.value)}
            placeholder="Add markdown notes here..."
            className="font-mono text-sm min-h-[150px]"
          />
        </div>

        {/* TODO: Contacts, Interviews, and Status History accordions */}
        <div className="rounded-lg border border-dashed border-gray-300 p-8 text-center text-sm text-gray-500">
          Contacts and Interview Logs coming soon.
        </div>
      </div>
    </Drawer>
  );
}
