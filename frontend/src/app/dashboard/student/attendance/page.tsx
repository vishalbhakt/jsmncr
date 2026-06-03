"use client";

import { useAuthStore } from "@/store/useAuthStore";
import DashboardLayout from "@/components/DashboardLayout";
import { useEffect, useState } from "react";
import api, { attendanceAPI } from "@/lib/api";
import { 
  Calendar as CalendarIcon, 
  CheckCircle2, 
  XCircle, 
  AlertCircle,
  PieChart
} from "lucide-react";
import { motion } from "framer-motion";
import { useToastStore } from "@/store/useToastStore";

export default function StudentAttendance() {
  const { user } = useAuthStore();
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const addToast = useToastStore(s => s.addToast);

  useEffect(() => {
    const fetchAttendance = async () => {
      try {
        const res = await attendanceAPI.list();
        setData(res.data.data);
      } catch {
        addToast("Failed to fetch attendance records", "error");
      } finally {
        setLoading(false);
      }
    };
    fetchAttendance();
  }, []);

  const stats = {
    present: data.filter(a => a.status === 'Present').length,
    absent: data.filter(a => a.status === 'Absent').length,
    late: data.filter(a => a.status === 'Late').length,
    total: data.length
  };

  const percentage = stats.total > 0 ? Math.round((stats.present / stats.total) * 100) : 0;

  if (!user) return null;

  return (
    <DashboardLayout>
      <div className="space-y-10 pb-20">
        <div>
          <h1 className="text-4xl font-black text-navy tracking-tight">
            Attendance Log
          </h1>
          <p className="text-slate-500 font-medium mt-1">
            Monitor your daily presence and track consistency.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
           <div className="bg-white p-8 rounded-[2.5rem] border border-navy/5 shadow-sm text-center space-y-2">
              <div className="text-4xl font-black text-navy">{percentage}%</div>
              <div className="text-[10px] font-black uppercase text-slate-400 tracking-widest">Attendance Rate</div>
           </div>
           <div className="bg-emerald-50 p-8 rounded-[2.5rem] border border-emerald-100 text-center space-y-2">
              <div className="text-4xl font-black text-emerald-600">{stats.present}</div>
              <div className="text-[10px] font-black uppercase text-emerald-400 tracking-widest">Days Present</div>
           </div>
           <div className="bg-rose-50 p-8 rounded-[2.5rem] border border-rose-100 text-center space-y-2">
              <div className="text-4xl font-black text-rose-600">{stats.absent}</div>
              <div className="text-[10px] font-black uppercase text-rose-400 tracking-widest">Days Absent</div>
           </div>
           <div className="bg-amber-50 p-8 rounded-[2.5rem] border border-amber-100 text-center space-y-2">
              <div className="text-4xl font-black text-amber-600">{stats.late}</div>
              <div className="text-[10px] font-black uppercase text-amber-400 tracking-widest">Late Arrivals</div>
           </div>
        </div>

        <div className="bg-white rounded-[2.5rem] border border-navy/5 shadow-sm overflow-hidden">
          <div className="p-8 border-b border-navy/5 flex items-center justify-between">
             <h3 className="text-xl font-bold text-navy">Detailed History</h3>
             <CalendarIcon className="w-5 h-5 text-slate-300" />
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="bg-slate-50/50 text-[10px] font-black uppercase tracking-widest text-slate-400">
                  <th className="px-8 py-5">Date</th>
                  <th className="px-6 py-5">Subject / Period</th>
                  <th className="px-8 py-5 text-center">Status</th>
                  <th className="px-8 py-5 text-right">Instructor</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-navy/5">
                {data.map((row, i) => (
                  <tr key={i} className="hover:bg-slate-50/50 transition-colors group">
                    <td className="px-8 py-5 font-bold text-navy">{new Date(row.date).toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short' })}</td>
                    <td className="px-6 py-5 font-medium text-slate-500">{row.subject_name || "Daily Attendance"}</td>
                    <td className="px-8 py-5">
                       <div className={`mx-auto w-fit px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest flex items-center gap-2 ${
                         row.status === 'Present' ? "bg-emerald-500/10 text-emerald-600" :
                         row.status === 'Absent' ? "bg-rose-500/10 text-rose-600" :
                         "bg-amber-500/10 text-amber-600"
                       }`}>
                          {row.status === 'Present' ? <CheckCircle2 className="w-3 h-3" /> : 
                           row.status === 'Absent' ? <XCircle className="w-3 h-3" /> : 
                           <AlertCircle className="w-3 h-3" />}
                          {row.status}
                       </div>
                    </td>
                    <td className="px-8 py-5 text-right text-slate-400 text-xs font-bold">{row.marked_by_name || "System"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {!data.length && !loading && (
            <div className="py-32 text-center text-slate-300 font-medium italic">No attendance logs found for your account.</div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}
