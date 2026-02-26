import { useState } from "react";
import { Modal } from "../ui/Modal";
import { Input } from "../ui/Input";
import { Button } from "../ui/Button";
import { useCreateApplication } from "../../hooks/useApplications";
import type { ApplicationStatus, ApplicationPriority } from "../../types";

const STATUS_LABELS: Record<ApplicationStatus, string> = {
  wishlist: "Wishlist",
  applied: "Applied",
  phone_screen: "Phone Screen",
  interview: "Interview",
  offer: "Offer",
  rejected: "Rejected",
  closed: "Closed",
};

interface CreateApplicationModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialStatus: ApplicationStatus;
}

export function CreateApplicationModal({
  isOpen,
  onClose,
  initialStatus,
}: CreateApplicationModalProps) {
  const { mutateAsync: createApplication, isPending } = useCreateApplication();

  const [companyName, setCompanyName] = useState("");
  const [roleTitle, setRoleTitle] = useState("");
  const [location, setLocation] = useState("");
  const [jobUrl, setJobUrl] = useState("");
  const [priority, setPriority] = useState<ApplicationPriority>("medium");
  const [appliedDate, setAppliedDate] = useState("");
  const [errors, setErrors] = useState<{
    companyName?: string;
    roleTitle?: string;
  }>({});

  const handleClose = () => {
    setCompanyName("");
    setRoleTitle("");
    setLocation("");
    setJobUrl("");
    setPriority("medium");
    setAppliedDate("");
    setErrors({});
    onClose();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const newErrors: typeof errors = {};
    if (!companyName.trim()) newErrors.companyName = "Company name is required";
    if (!roleTitle.trim()) newErrors.roleTitle = "Role title is required";
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    try {
      await createApplication({
        company_name: companyName.trim(),
        role_title: roleTitle.trim(),
        location: location.trim() || undefined,
        job_url: jobUrl.trim() || undefined,
        priority,
        applied_date: appliedDate || undefined,
        status: initialStatus,
      });
      handleClose();
    } catch {
      // server error — keep modal open so user can retry
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title="Add Job Application"
      footer={
        <div className="flex w-full gap-3 justify-end">
          <Button
            variant="secondary"
            onClick={handleClose}
            disabled={isPending}
          >
            Cancel
          </Button>
          <Button
            form="create-application-form"
            type="submit"
            isLoading={isPending}
          >
            Add Application
          </Button>
        </div>
      }
    >
      <form
        id="create-application-form"
        onSubmit={handleSubmit}
        className="space-y-4"
      >
        <div className="rounded-md bg-gray-50 px-3 py-2 text-sm text-gray-600">
          Adding to:{" "}
          <span className="font-medium text-gray-900">
            {STATUS_LABELS[initialStatus]}
          </span>
        </div>

        <Input
          id="company-name"
          label="Company *"
          placeholder="e.g. Acme Corp"
          value={companyName}
          onChange={(e) => {
            setCompanyName(e.target.value);
            if (errors.companyName)
              setErrors((prev) => ({ ...prev, companyName: undefined }));
          }}
          error={errors.companyName}
          autoFocus
        />

        <Input
          id="role-title"
          label="Role *"
          placeholder="e.g. Senior Software Engineer"
          value={roleTitle}
          onChange={(e) => {
            setRoleTitle(e.target.value);
            if (errors.roleTitle)
              setErrors((prev) => ({ ...prev, roleTitle: undefined }));
          }}
          error={errors.roleTitle}
        />

        <Input
          id="location"
          label="Location"
          placeholder="e.g. San Francisco, CA (Remote)"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />

        <Input
          id="job-url"
          label="Job URL"
          type="url"
          placeholder="https://..."
          value={jobUrl}
          onChange={(e) => setJobUrl(e.target.value)}
        />

        <div className="flex gap-4">
          <div className="flex-1 space-y-1">
            <label
              htmlFor="priority"
              className="block text-sm font-medium text-gray-700"
            >
              Priority
            </label>
            <select
              id="priority"
              value={priority}
              onChange={(e) =>
                setPriority(e.target.value as ApplicationPriority)
              }
              className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          <div className="flex-1 space-y-1">
            <label
              htmlFor="applied-date"
              className="block text-sm font-medium text-gray-700"
            >
              Applied Date
            </label>
            <input
              id="applied-date"
              type="date"
              value={appliedDate}
              onChange={(e) => setAppliedDate(e.target.value)}
              className="flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-colors"
            />
          </div>
        </div>
      </form>
    </Modal>
  );
}
