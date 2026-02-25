import type { FormEvent } from "react";
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { authApi } from "../api/auth";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";

export function Register() {
  const [formData, setFormData] = useState({
    email: "",
    full_name: "",
    password: "",
    confirm_password: "",
  });
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");

    if (formData.password !== formData.confirm_password) {
      setError("Passwords do not match");
      return;
    }

    setIsLoading(true);

    try {
      await authApi.register({
        email: formData.email,
        full_name: formData.full_name,
        password: formData.password,
      });
      navigate("/login", {
        state: { message: "Registration successful! Please sign in." },
      });
    } catch (err: unknown) {
      console.error(err);
      const axiosError = err as {
        response?: { data?: Record<string, string[]> };
      };
      const outputError = axiosError.response?.data
        ? Object.values(axiosError.response?.data).join(" ")
        : "Registration failed. Please try again.";
      setError(outputError as string);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8 rounded-xl bg-white p-10 shadow-lg border border-gray-100">
        <div>
          <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
            Create an account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Already have an account?{" "}
            <Link
              to="/login"
              className="font-medium text-indigo-600 hover:text-indigo-500"
            >
              Sign in
            </Link>
          </p>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="rounded-md bg-red-50 p-4 border border-red-200">
              <div className="flex">
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">{error}</h3>
                </div>
              </div>
            </div>
          )}
          <div className="space-y-4">
            <Input
              id="full_name"
              name="full_name"
              type="text"
              required
              label="Full Name"
              placeholder="John Doe"
              value={formData.full_name}
              onChange={handleChange}
            />
            <Input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              label="Email address"
              placeholder="you@example.com"
              value={formData.email}
              onChange={handleChange}
            />
            <Input
              id="password"
              name="password"
              type="password"
              required
              label="Password"
              placeholder="••••••••"
              value={formData.password}
              onChange={handleChange}
            />
            <Input
              id="confirm_password"
              name="confirm_password"
              type="password"
              required
              label="Confirm Password"
              placeholder="••••••••"
              value={formData.confirm_password}
              onChange={handleChange}
              error={
                formData.password &&
                formData.confirm_password &&
                formData.password !== formData.confirm_password
                  ? "Passwords don't match"
                  : undefined
              }
            />
          </div>

          <div>
            <Button type="submit" className="w-full" isLoading={isLoading}>
              Register
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
