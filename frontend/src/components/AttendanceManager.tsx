"use client";

import { useState, useEffect } from "react";
import api from "@/lib/api";
import { Check, X, Save, Calendar, User, Loader2 } from "lucide-react";
import { useToastStore } from "@/store/useToastStore";

export default function AttendanceManager({ subjects }: { subjects: any[] }) {
  const [selectedSubject, setSelectedSubject] = useState("");
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [students, setStudents] = useState<any[]>([]);
  const [attendance, setAttendance] = useState<Record<number, string>>({});
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const addToast = useToastStore(s => s.addToast);

  const fetchStudents = async () => {
    if (!selectedSubject) return;
    setLoading(true);
    try {
      // Fetch students for the course associated with the subject
      const sub = subjects.find(s => s.id === parseInt(selectedSubject));
      const res = await api.get(`/students/?course=${sub.course}`);
      setStudents(res.data.data);
      
      // Initialize attendance state (all present by default)
      const initial: Record<number, string> = {};
      res.data.data.forEach((s: any) => initial[s.id] = 'Present');
      setAttendance(initial);
    } catch {
      addToast("Failed to fetch students", "error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStudents();
  }, [selectedSubject]);

  const handleMark = async () => {
    if (!selectedSubject) return;
    setSaving(true);
    const payload = Object.entries(attendance).map(([id, status]) => ({
      student: parseInt(id),
      status,
      date,
      subject: parseInt(selectedSubject)
    }));

    try {
      const res = await api.post("/attendance/bulk_mark/", payload);
      if (res.data.success) {
        addToast("Attendance saved successfully!");
      } else {
        const errorMsg = typeof res.data.error === 'object' 
          ? Object.entries(res.data.error).map(([k, v]) => `${k}: ${v}`).join(", ")
          : res.data.error || "Failed to save attendance";
        addToast(errorMsg, "error");
      }
    } catch (err: any) {
      const msg = err.response?.data?.error || "Connection error occurred.";
      addToast(msg, "error");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="bg-white p-8 rounded-[2.5rem] border border-navy/5 shadow-sm grid grid-cols-1 md:grid-cols-2 gap-6 items-end">
        <div className="space-y-2">
          <label className="text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1">Select Subject</label>
          <select 
            className="w-full bg-slate-50 border-2 border-slate-100 rounded-2xl px-4 py-3 font-bold focus:border-gold outline-none transition-all"
            value={selectedSubject}
            onChange={e => setSelectedSubject(e.target.value)}
          >
            <option value="">-- Choose Subject --</option>
            {subjects.map(s => <option key={s.id} value={s.id}>{s.name} ({s.course_name})</option>)}
          </select>
        </div>
        <div className="space-y-2">
          <label className="text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1">Attendance Date</label>
          <div className="relative">
            <Calendar className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-300" />
            <input 
              type="date" 
              className="w-full bg-slate-50 border-2 border-slate-100 rounded-2xl pl-12 pr-4 py-3 font-bold focus:border-gold outline-none transition-all"
              value={date}
              onChange={e => setDate(e.target.value)}
            />
          </div>
        </div>
      </div>

      {selectedSubject && (
        <div className="bg-white rounded-[2.5rem] border border-navy/5 shadow-sm overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-500">
           {loading ? (
             <div className="p-20 text-center">
                <Loader2 className="w-10 h-10 animate-spin text-gold mx-auto mb-4" />
                <p className="text-slate-400 font-bold uppercase tracking-widest text-xs">Loading Class Register...</p>
             </div>
           ) : (
             <>
               <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="bg-slate-50/50 border-b border-navy/5 text-[10px] font-black uppercase tracking-widest text-slate-400">
                      <th className="px-8 py-5 w-20 text-center">#</th>
                      <th className="px-6 py-5">Student Name</th>
                      <th className="px-6 py-5">Roll No.</th>
                      <th className="px-8 py-5 text-center">Mark Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-navy/5">
                    {students.map((s, i) => (
                      <tr key={s.id} className="hover:bg-slate-50/50 transition-colors">
                        <td className="px-8 py-5 text-center text-slate-300 font-black">{i+1}</td>
                        <td className="px-6 py-5">
                          <div className="flex items-center gap-3">
                             <div className="w-8 h-8 bg-navy/5 rounded-full flex items-center justify-center text-navy font-black text-xs">{(s.user.first_name?.[0] || s.user.username?.[0] || "?").toUpperCase()}</div>
                             <div className="font-bold text-navy">{s.user.first_name} {s.user.last_name}</div>
                          </div>
                        </td>
                        <td className="px-6 py-5 font-bold text-slate-400">{s.roll_number}</td>
                        <td className="px-8 py-5">
                          <div className="flex items-center justify-center gap-2 bg-slate-100 p-1.5 rounded-2xl w-fit mx-auto">
                            {['Present', 'Absent', 'Late'].map(status => (
                              <button
                                key={status}
                                onClick={() => setAttendance({...attendance, [s.id]: status})}
                                className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${
                                  attendance[s.id] === status 
                                    ? (status === 'Present' ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/20' : 
                                       status === 'Absent' ? 'bg-red-500 text-white shadow-lg shadow-red-500/20' : 
                                       'bg-amber-500 text-white shadow-lg shadow-amber-500/20')
                                    : 'text-slate-400 hover:text-navy'
                                }`}
                              >
                                {status}
                              </button>
                            ))}
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
               </table>
               
               <div className="p-8 border-t border-navy/5 bg-slate-50/30 flex justify-end">
                  <button 
                    onClick={handleMark} 
                    disabled={saving}
                    className="btn-primary flex items-center gap-3 shadow-xl shadow-navy/10 disabled:opacity-70"
                  >
                    {saving ? (
                      <><Loader2 className="w-5 h-5 animate-spin" /> Saving Log...</>
                    ) : (
                      <><Save className="w-5 h-5" /> Save Attendance Log</>
                    )}
                  </button>
               </div>
             </>
           )}
        </div>
      )}

      {!selectedSubject && (
        <div className="py-32 text-center text-slate-400 font-medium italic bg-white rounded-[2.5rem] border-2 border-dashed border-navy/5">
          Please select a subject above to load the class register.
        </div>
      )}
    </div>
  );
}
