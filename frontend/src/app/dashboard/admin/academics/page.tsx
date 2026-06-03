"use client";

import { useAuthStore } from "@/store/useAuthStore";
import DashboardLayout from "@/components/DashboardLayout";
import { useEffect, useState } from "react";
import api, { coursesAPI, subjectsAPI } from "@/lib/api";
import { 
  GraduationCap, 
  BookOpen, 
  Plus, 
  Trash2, 
  ChevronRight,
  ShieldAlert
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useToastStore } from "@/store/useToastStore";

export default function AdminAcademics() {
  const { user } = useAuthStore();
  const [courses, setCourses] = useState<any[]>([]);
  const [subjects, setSubjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isAdding, setIsAdding] = useState<string | null>(null);
  const [form, setForm] = useState({ name: "", description: "", course: "" });
  const addToast = useToastStore(s => s.addToast);

  const fetchData = async () => {
    try {
      const [cRes, sRes] = await Promise.all([
        coursesAPI.list(),
        subjectsAPI.list()
      ]);
      setCourses(cRes.data.data);
      setSubjects(sRes.data.data);
    } catch {
      addToast("Failed to fetch academic data", "error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (isAdding === 'course') await coursesAPI.create(form);
      else await subjectsAPI.create(form);
      
      addToast(`${isAdding} added successfully!`);
      setIsAdding(null);
      setForm({ name: "", description: "", course: "" });
      fetchData();
    } catch {
      addToast("Failed to save entry", "error");
    }
  };

  const handleDelete = async (type: 'course' | 'subject', id: number) => {
    if (!confirm(`Delete this ${type}? This will remove all related data.`)) return;
    try {
      if (type === 'course') await coursesAPI.delete(id);
      else await subjectsAPI.delete(id);
      addToast(`${type} removed.`);
      fetchData();
    } catch {
      addToast("Delete failed", "error");
    }
  };

  if (!user) return null;

  return (
    <DashboardLayout>
      <div className="space-y-10 pb-20">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <h1 className="text-4xl font-black text-navy tracking-tight">
              Academic Infrastructure
            </h1>
            <p className="text-slate-500 font-medium mt-1">
              Define and manage the school's courses and subject offerings.
            </p>
          </div>
          <div className="flex gap-4">
             <button onClick={() => setIsAdding('course')} className="btn-primary flex items-center gap-2">
                <Plus className="w-4 h-4" /> New Course
             </button>
             <button onClick={() => setIsAdding('subject')} className="btn-gold flex items-center gap-2">
                <Plus className="w-4 h-4" /> New Subject
             </button>
          </div>
        </div>

        <AnimatePresence>
          {isAdding && (
            <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="bg-white p-10 rounded-[3rem] border-2 border-gold/20 shadow-2xl space-y-8">
               <h3 className="text-2xl font-black text-navy capitalize">Add New {isAdding}</h3>
               <form onSubmit={handleAdd} className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                     <label className="text-[10px] font-black uppercase text-slate-400 ml-1">Name</label>
                     <input required className="w-full bg-slate-50 border-2 border-slate-100 rounded-2xl px-5 py-4 font-bold outline-none focus:border-gold"
                       value={form.name} onChange={e => setForm({...form, name: e.target.value})} />
                  </div>
                  {isAdding === 'subject' && (
                    <div className="space-y-2">
                      <label className="text-[10px] font-black uppercase text-slate-400 ml-1">Parent Course</label>
                      <select required className="w-full bg-slate-50 border-2 border-slate-100 rounded-2xl px-5 py-4 font-bold outline-none focus:border-gold"
                        value={form.course} onChange={e => setForm({...form, course: e.target.value})}>
                        <option value="">-- Choose Course --</option>
                        {courses.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                      </select>
                    </div>
                  )}
                  <div className="col-span-2 space-y-2">
                     <label className="text-[10px] font-black uppercase text-slate-400 ml-1">Description</label>
                     <textarea className="w-full bg-slate-50 border-2 border-slate-100 rounded-2xl px-5 py-4 font-bold outline-none focus:border-gold min-h-[100px]"
                       value={form.description} onChange={e => setForm({...form, description: e.target.value})} />
                  </div>
                  <div className="col-span-2 flex gap-4 pt-4 border-t border-navy/5">
                     <button type="button" onClick={() => setIsAdding(null)} className="flex-1 font-black text-slate-400 uppercase tracking-widest text-xs">Cancel</button>
                     <button type="submit" className="flex-1 btn-primary py-4 uppercase font-black tracking-widest text-xs shadow-xl">Create {isAdding}</button>
                  </div>
               </form>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
           {/* Courses */}
           <div className="bg-white rounded-[2.5rem] border border-navy/5 shadow-sm p-8 space-y-8 flex flex-col h-[600px]">
              <div className="flex items-center justify-between">
                 <h3 className="text-xl font-bold text-navy flex items-center gap-3"><GraduationCap className="text-gold" /> Available Courses</h3>
                 <span className="px-3 py-1 bg-navy/5 text-navy rounded-lg text-[10px] font-black">{courses.length}</span>
              </div>
              <div className="flex-1 overflow-auto space-y-4 pr-2 custom-scrollbar">
                 {Array.isArray(courses) && courses.map(c => (
                   <div key={c.id} className="p-6 bg-slate-50 rounded-3xl border border-navy/5 flex justify-between items-center group hover:bg-white hover:shadow-lg transition-all">
                      <div>
                         <div className="font-bold text-navy">{c.name}</div>
                         <div className="text-[10px] text-slate-400 font-bold uppercase tracking-widest mt-1">{c.student_count || 0} Students Enrolled</div>
                      </div>
                      <button onClick={() => handleDelete('course', c.id)} className="p-2 text-slate-300 hover:text-rose-500 opacity-0 group-hover:opacity-100 transition-all"><Trash2 className="w-4 h-4" /></button>
                   </div>
                 ))}
              </div>
           </div>

           {/* Subjects */}
           <div className="bg-white rounded-[2.5rem] border border-navy/5 shadow-sm p-8 space-y-8 flex flex-col h-[600px]">
              <div className="flex items-center justify-between">
                 <h3 className="text-xl font-bold text-navy flex items-center gap-3"><BookOpen className="text-gold" /> Defined Subjects</h3>
                 <span className="px-3 py-1 bg-navy/5 text-navy rounded-lg text-[10px] font-black">{subjects.length}</span>
              </div>
              <div className="flex-1 overflow-auto space-y-4 pr-2 custom-scrollbar">
                 {Array.isArray(subjects) && subjects.map(s => (
                   <div key={s.id} className="p-6 bg-slate-50 rounded-3xl border border-navy/5 flex justify-between items-center group hover:bg-white hover:shadow-lg transition-all">
                      <div>
                         <div className="font-bold text-navy">{s.name}</div>
                         <div className="text-[10px] text-gold font-black uppercase tracking-widest mt-1">{s.course_name}</div>
                      </div>
                      <button onClick={() => handleDelete('subject', s.id)} className="p-2 text-slate-300 hover:text-rose-500 opacity-0 group-hover:opacity-100 transition-all"><Trash2 className="w-4 h-4" /></button>
                   </div>
                 ))}
              </div>
           </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
