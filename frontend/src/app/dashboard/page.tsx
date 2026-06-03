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
  ArrowUpRight 
} from "lucide-react";

export default function DashboardPage() {
  const { user } = useAuthStore();
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get("/dashboard/stats/");
        setStats(res.data.data);
      } catch (err) {
        console.error("Failed to fetch stats");
      }
    };
    fetchStats();
  }, []);

  if (!user) return null;

  return (
    <DashboardLayout>
      <div className="space-y-10">
        {/* Welcome Section */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <h1 className="text-4xl font-black text-navy tracking-tight">
              Hello, {user.first_name || user.username} 👋
            </h1>
            <p className="text-slate-500 font-medium mt-1">
              Welcome back to your {user.role.toLowerCase()} command center.
            </p>
          </div>
          <div className="flex items-center gap-2 bg-white px-4 py-2 rounded-2xl border border-navy/5 shadow-sm">
            <Clock className="w-4 h-4 text-gold" />
            <span className="text-sm font-bold text-navy">
              {new Date().toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'long' })}
            </span>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {user.role === 'ADMIN' && (
            <>
              <StatCard icon={Users} label="Total Students" value={stats?.total_students} color="bg-blue-500" />
              <StatCard icon={CheckCircle} label="Pending Approvals" value={stats?.pending_approvals} color="bg-amber-500" />
              <StatCard icon={BookOpen} label="Active Courses" value={stats?.total_courses} color="bg-emerald-500" />
              <StatCard icon={Users} label="Total Teachers" value={stats?.total_teachers} color="bg-indigo-500" />
            </>
          )}
          {user.role === 'TEACHER' && (
            <>
              <StatCard icon={BookOpen} label="My Subjects" value={stats?.my_subjects?.length} color="bg-indigo-500" />
              <StatCard icon={CheckCircle} label="Assignments" value={stats?.my_assignments} color="bg-emerald-500" />
            </>
          )}
          {user.role === 'STUDENT' && (
            <>
              <StatCard icon={CheckCircle} label="Attendance" value={`${stats?.attendance_percentage}%`} color="bg-emerald-500" />
              <StatCard icon={Clock} label="Pending Fees" value={stats?.pending_payments} color="bg-rose-500" />
            </>
          )}
        </div>

        {/* Recent Activity / Announcements */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 bg-white rounded-3xl border border-navy/5 p-8 shadow-sm">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-navy">Recent Announcements</h3>
              <button className="text-gold text-xs font-black uppercase tracking-widest hover:text-gold-dark transition-all">View All</button>
            </div>
            <div className="space-y-4">
              {stats?.recent_announcements?.map((a: any) => (
                <div key={a.id} className="group flex items-center justify-between p-4 rounded-2xl hover:bg-pearl transition-all border border-transparent hover:border-navy/5">
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 bg-navy/5 rounded-xl flex items-center justify-center text-navy font-black text-xs group-hover:bg-gold/10 group-hover:text-gold transition-all">
                      {a.audience[0]}
                    </div>
                    <div>
                      <div className="font-bold text-navy">{a.title}</div>
                      <div className="text-xs text-slate-400 font-medium">To: {a.audience} • {new Date(a.created_at).toLocaleDateString()}</div>
                    </div>
                  </div>
                  <ArrowUpRight className="w-5 h-5 text-slate-300 group-hover:text-gold transition-all" />
                </div>
              ))}
              {!stats?.recent_announcements?.length && (
                <div className="text-center py-10 text-slate-400 font-medium italic">No new announcements today.</div>
              )}
            </div>
          </div>

          <div className="bg-navy rounded-3xl p-8 text-white shadow-xl relative overflow-hidden">
            <div className="relative z-10 space-y-6">
              <h3 className="text-xl font-bold text-gold">System Health</h3>
              <p className="text-white/60 text-sm leading-relaxed">
                Your production environment is running smoothly. All services are operational.
              </p>
              <div className="pt-4">
                <div className="flex justify-between text-xs font-bold uppercase tracking-widest text-white/40 mb-2">
                  <span>Server Load</span>
                  <span>Normal</span>
                </div>
                <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
                  <div className="h-full bg-gold w-[35%] rounded-full shadow-[0_0_10px_rgba(201,162,39,0.5)]"></div>
                </div>
              </div>
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
    <div className="bg-white p-6 rounded-3xl border border-navy/5 shadow-sm group hover:border-gold/30 transition-all">
      <div className={`w-12 h-12 ${color} bg-opacity-10 rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
        <Icon className={`w-6 h-6 ${color.replace('bg-', 'text-')}`} />
      </div>
      <div className="text-2xl font-black text-navy">{value ?? 0}</div>
      <div className="text-xs font-bold text-slate-400 uppercase tracking-wider mt-1">{label}</div>
    </div>
  );
}
