"use client";

import { useAuthStore } from "@/store/useAuthStore";
import DashboardLayout from "@/components/DashboardLayout";
import { useEffect, useState } from "react";
import api, { notesAPI, subjectsAPI } from "@/lib/api";
import { 
  Plus, 
  Trash2, 
  FileText, 
  Send,
  Loader2,
  MoreVertical,
  Download
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useToastStore } from "@/store/useToastStore";

export default function TeacherNotes() {
  const { user } = useAuthStore();
  const [items, setItems] = useState<any[]>([]);
  const [subjects, setSubjects] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isAdding, setIsAdding] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({ title: "", content: "", subject: "" });
  const [file, setFile] = useState<File | null>(null);
  const addToast = useToastStore(s => s.addToast);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [itemRes, subRes] = await Promise.all([
        notesAPI.list(),
        subjectsAPI.list()
      ]);
      setItems(itemRes.data.data);
      setSubjects(subRes.data.data);
    } catch {
      addToast("Failed to sync notes repository", "error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    const fd = new FormData();
    Object.keys(form).forEach(k => fd.append(k, (form as any)[k]));
    if (file) fd.append("file", file);

    try {
      const res = await notesAPI.create(fd);
      if (res.data.success) {
        setIsAdding(false);
        setForm({ title: "", content: "", subject: "" });
        setFile(null);
        addToast("Notes published successfully!");
        fetchData();
      } else {
        const errorMsg = typeof res.data.error === 'object' 
          ? Object.entries(res.data.error).map(([k, v]) => `${k}: ${v}`).join(", ")
          : res.data.error || "Failed to publish notes";
        addToast(errorMsg, "error");
      }
    } catch (err: any) {
      const msg = err.response?.data?.error || "Failed to connect to repository.";
      addToast(msg, "error");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete these notes?")) return;
    try {
      await notesAPI.delete(id);
      setItems(items.filter(i => i.id !== id));
      addToast("Notes removed.");
    } catch {
      addToast("Action failed", "error");
    }
  };

  if (!user) return null;

  return (
    <DashboardLayout>
      <div className="space-y-10 pb-20">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <h1 className="text-4xl font-black text-navy tracking-tight">
              Study Materials
            </h1>
            <p className="text-slate-500 font-medium mt-1">
              Upload and organize academic notes for your classes.
            </p>
          </div>
          <button 
            onClick={() => setIsAdding(!isAdding)}
            className={`flex items-center gap-2 px-8 py-3.5 rounded-2xl font-black text-xs uppercase tracking-widest transition-all ${
              isAdding ? "bg-slate-100 text-slate-500" : "bg-gold text-navy shadow-xl shadow-gold/20"
            }`}
          >
            {isAdding ? "Cancel" : <><Plus className="w-4 h-4" /> Upload Notes</>}
          </button>
        </div>

        <AnimatePresence>
          {isAdding && (
            <motion.div 
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="bg-white rounded-[3rem] border-2 border-gold/20 p-10 shadow-2xl relative overflow-hidden"
            >
              <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-8 relative z-10">
                <div className="col-span-2 space-y-2">
                  <label className="text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1">Note Title</label>
                  <input required className="w-full bg-slate-50 border-2 border-slate-100 rounded-2xl px-6 py-4 font-bold focus:border-gold outline-none transition-all"
                    placeholder="e.g. Chapter 5: Linear Equations"
                    value={form.title} onChange={e => setForm({...form, title: e.target.value})} />
                </div>
                <div className="col-span-2 space-y-2">
                  <label className="text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1">Short Description</label>
                  <textarea className="w-full bg-slate-50 border-2 border-slate-100 rounded-2xl px-6 py-4 font-bold focus:border-gold outline-none min-h-[100px] transition-all"
                    placeholder="Briefly explain what these notes cover..."
                    value={form.content} onChange={e => setForm({...form, content: e.target.value})} />
                </div>
                <div className="space-y-2">
                  <label className="text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1">Subject</label>
                  <select required className="w-full bg-slate-50 border-2 border-slate-100 rounded-2xl px-6 py-4 font-bold focus:border-gold outline-none appearance-none cursor-pointer"
                    value={form.subject} onChange={e => setForm({...form, subject: e.target.value})}>
                    <option value="">-- Select Subject --</option>
                    {Array.isArray(subjects) && subjects.map(s => <option key={s.id} value={s.id}>{s.name} ({s.course_name})</option>)}
                  </select>
                </div>
                <div className="space-y-2">
                  <label className="text-[10px] font-black uppercase tracking-widest text-slate-400 ml-1">Upload PDF/Document</label>
                  <input type="file" className="w-full bg-slate-50 border-2 border-slate-100 rounded-2xl px-6 py-4 font-bold focus:border-gold outline-none"
                    onChange={e => setFile(e.target.files?.[0] || null)} />
                </div>
                <button 
                  type="submit" 
                  disabled={saving}
                  className="col-span-2 btn-primary py-5 rounded-2xl flex items-center justify-center gap-3 shadow-xl shadow-navy/20 uppercase tracking-[0.2em] font-black text-xs disabled:opacity-70"
                >
                  {saving ? (
                    <><Loader2 className="w-5 h-5 animate-spin" /> Publishing...</>
                  ) : (
                    <><Send className="w-5 h-5" /> Publish to Repository</>
                  )}
                </button>
              </form>
            </motion.div>
          )}
        </AnimatePresence>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[1,2,3].map(i => <div key={i} className="h-64 bg-white rounded-[2.5rem] animate-pulse border border-navy/5"></div>)}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {items.map((item) => (
              <div key={item.id} className="bg-white p-8 rounded-[2.5rem] border border-navy/5 shadow-sm hover:border-gold/30 transition-all flex flex-col group relative">
                <div className="flex items-center justify-between mb-6">
                   <div className="px-3 py-1 bg-gold/10 text-gold text-[10px] font-black uppercase tracking-widest rounded-lg">{item.subject_name}</div>
                   <button onClick={() => handleDelete(item.id)} className="p-2 text-slate-200 hover:text-rose-500 transition-colors"><Trash2 className="w-4 h-4" /></button>
                </div>

                <h3 className="text-xl font-black text-navy mb-3 line-clamp-1">{item.title}</h3>
                <p className="text-slate-400 text-sm font-medium line-clamp-3 mb-10 leading-relaxed italic">"{item.content}"</p>
                
                <div className="mt-auto pt-6 border-t border-navy/5 flex items-center justify-between">
                   <div className="text-[10px] font-black text-slate-300 uppercase tracking-widest">{new Date(item.created_at).toLocaleDateString()}</div>
                   {item.file && (
                     <a href={item.file} target="_blank" className="w-12 h-12 bg-navy text-white rounded-2xl flex items-center justify-center hover:bg-gold transition-all shadow-xl active:scale-90">
                        <Download className="w-5 h-5" />
                     </a>
                   )}
                </div>
              </div>
            ))}
            {!items.length && !isAdding && (
              <div className="col-span-full py-40 text-center bg-white rounded-[3rem] border-2 border-dashed border-navy/5 flex flex-col items-center">
                 <div className="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mb-6">
                    <FileText className="w-10 h-10 text-slate-200" />
                 </div>
                 <p className="text-slate-400 font-bold uppercase tracking-widest text-xs">Your notes repository is currently empty.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
