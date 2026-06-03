"use client";

import { useAuthStore } from "@/store/useAuthStore";
import DashboardLayout from "@/components/DashboardLayout";
import { useEffect, useState } from "react";
import api from "@/lib/api";
import { 
  Users, 
  BookOpen, 
  CheckCircle, 
  Clock, 
  ArrowUpRight,
  Calendar
} from "lucide-react";
import { motion } from "framer-motion";

export default function TeacherOverview() {
  const { user } = useAuthStore();
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get("/dashboard/stats/");
        setStats(res.data.data);
      } catch (err) {
        console.error("Stats fetch failed");
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (!user) return null;

  return (
    <DashboardLayout>
      <div className="space-y-10 pb-20">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <h1 className="text-4xl font-black text-navy tracking-tight">
              Hi, {user.first_name || user.username} 🏫
            </h1>
            <p className="text-slate-500 font-medium mt-1">
              Manage your daily academic operations.
            </p>
          </div>
          <div className="flex items-center gap-3 bg-white px-5 py-3 rounded-2xl border border-navy/5 shadow-sm">
             <Calendar className="w-5 h-5 text-gold" />
             <span className="text-sm font-black text-navy uppercase tracking-widest">
               {new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}
             </span>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
           <StatCard icon={BookOpen} label="My Subjects" value={stats?.my_subjects} color="bg-indigo-500" />
           <StatCard icon={CheckCircle} label="Assignments" value={stats?.my_assignments} color="bg-emerald-500" />
           <StatCard icon={Users} label="Total Students" value={stats?.total_students} color="bg-blue-500" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
           <div className="bg-white p-8 rounded-[2.5rem] border border-navy/5 shadow-sm">
             <h3 className="text-xl font-bold text-navy mb-6">Recent Announcements</h3>
             <div className="space-y-4">
                {stats?.recent_announcements?.map((a: any) => (
                  <div key={a.id} className="p-4 bg-slate-50 rounded-2xl border border-navy/5">
                    <div className="font-bold text-navy text-sm">{a.title}</div>
                    <div className="text-[10px] text-slate-400 font-black uppercase tracking-widest mt-1">{new Date(a.created_at).toLocaleDateString()}</div>
                  </div>
                ))}
                {!stats?.recent_announcements?.length && (
                  <div className="text-center py-10 text-slate-300 italic font-medium">No announcements yet.</div>
                )}
             </div>
           </div>
           <div className="bg-navy p-8 rounded-[2.5rem] text-white shadow-xl flex flex-col justify-center relative overflow-hidden">
             <div className="relative z-10">
                <h3 className="text-2xl font-black text-gold mb-2">Teacher Pro-Tip</h3>
                <p className="text-white/60 font-medium italic">"Use the Bulk Attendance feature to save time during morning roll call."</p>
             </div>
             <div className="absolute -bottom-10 -right-10 w-40 h-40 bg-gold/5 rounded-full blur-3xl"></div>
           </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

function StatCard({ icon: Icon, label, value, color }: any) {
  return (
    <div className="bg-white p-8 rounded-[2.5rem] border border-navy/5 shadow-sm group hover:border-gold/30 transition-all flex flex-col justify-between h-48">
      <div className={`w-14 h-14 ${color} bg-opacity-10 rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
        <Icon className={`w-7 h-7 ${color.replace('bg-', 'text-')}`} />
      </div>
      <div>
        <div className="text-3xl font-black text-navy leading-none">{value ?? 0}</div>
        <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mt-2">{label}</div>
      </div>
    </div>
  );
}
