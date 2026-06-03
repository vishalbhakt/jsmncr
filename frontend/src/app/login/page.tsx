"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import { useAuthStore } from "@/store/useAuthStore";
import Link from "next/link";
import { LogIn, Loader2, AlertCircle } from "lucide-react";

export default function LoginPage() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();
  const setAuth = useAuthStore((state) => state.setAuth);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const res = await api.post("/auth/login/", form);
      const { access, user } = res.data.data;
      setAuth(user, access);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.error || "Invalid credentials or pending approval.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-navy flex items-center justify-center p-6">
      <div className="w-full max-w-md bg-white rounded-3xl p-8 shadow-2xl space-y-8">
        <div className="text-center space-y-2">
          <img src="/logo.png" alt="JSM Logo" className="w-24 h-24 object-contain mx-auto mb-4" />
          <h2 className="text-3xl font-black text-navy">Welcome Back</h2>
          <p className="text-slate-400 font-medium">Access your school portal</p>
        </div>

        {error && (
          <div className="bg-red-50 text-red-600 p-4 rounded-xl flex items-center gap-3 text-sm font-bold border border-red-100">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="space-y-1.5">
            <label className="text-xs font-black uppercase tracking-widest text-slate-400">Username</label>
            <input
              type="text"
              required
              className="w-full bg-slate-50 border-2 border-slate-100 rounded-xl px-4 py-3 text-navy font-bold focus:border-gold outline-none transition-all"
              value={form.username}
              onChange={(e) => setForm({ ...form, username: e.target.value })}
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-black uppercase tracking-widest text-slate-400">Password</label>
            <input
              type="password"
              required
              className="w-full bg-slate-50 border-2 border-slate-100 rounded-xl px-4 py-3 text-navy font-bold focus:border-gold outline-none transition-all"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-navy text-white py-4 rounded-xl font-black text-sm tracking-widest uppercase flex items-center justify-center gap-2 transition-all hover:bg-navy-light active:scale-95 disabled:opacity-50"
          >
            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Sign In →"}
          </button>
        </form>

        <div className="text-center pt-4 border-t border-slate-100">
          <p className="text-slate-400 text-sm font-bold">
            Don't have an account?{" "}
            <Link href="/register" className="text-gold hover:text-gold-light transition-all">
              Register here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
