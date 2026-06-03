"use client";

import { useAuthStore } from "@/store/useAuthStore";
import DashboardLayout from "@/components/DashboardLayout";
import { useEffect, useState } from "react";
import api, { notesAPI, videoLecturesAPI } from "@/lib/api";
import { 
  FileText, 
  Video, 
  Download, 
  Play,
  Search,
  BookOpen
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useToastStore } from "@/store/useToastStore";

export default function StudentLearning() {
  const { user } = useAuthStore();
  const [notes, setNotes] = useState<any[]>([]);
  const [videos, setVideos] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState('notes');
  const [search, setSearch] = useState('');
  const addToast = useToastStore(s => s.addToast);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [noteRes, vidRes] = await Promise.all([
          notesAPI.list(),
          videoLecturesAPI.list()
        ]);
        setNotes(noteRes.data.data);
        setVideos(vidRes.data.data);
      } catch {
        addToast("Failed to fetch learning materials", "error");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const filteredData = (tab === 'notes' ? notes : videos).filter(item => 
    item.title.toLowerCase().includes(search.toLowerCase()) ||
    item.subject_name.toLowerCase().includes(search.toLowerCase())
  );

  if (!user) return null;

  return (
    <DashboardLayout>
      <div className="space-y-10 pb-20">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-8">
          <div>
            <h1 className="text-4xl font-black text-navy tracking-tight">
              Learning Hub
            </h1>
            <p className="text-slate-500 font-medium mt-1">
              Access your digital library of notes and video lessons.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 items-center">
            {/* Search */}
            <div className="relative w-full sm:w-64 group">
               <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-300 group-focus-within:text-gold transition-all" />
               <input 
                 placeholder="Search by title or subject..."
                 className="w-full bg-white border border-navy/5 rounded-2xl pl-12 pr-4 py-3 text-sm font-bold text-navy focus:border-gold outline-none shadow-sm transition-all"
                 value={search}
                 onChange={e => setSearch(e.target.value)}
               />
            </div>
            
            {/* Tabs */}
            <div className="flex p-1.5 bg-navy/5 rounded-2xl w-full sm:w-auto">
              <button 
                onClick={() => setTab('notes')}
                className={`flex-1 sm:flex-none flex items-center justify-center gap-2 px-6 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest transition-all ${
                  tab === 'notes' ? "bg-white text-navy shadow-sm" : "text-slate-400 hover:text-navy"
                }`}
              >
                <FileText className="w-4 h-4" /> Notes
              </button>
              <button 
                onClick={() => setTab('videos')}
                className={`flex-1 sm:flex-none flex items-center justify-center gap-2 px-6 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest transition-all ${
                  tab === 'videos' ? "bg-white text-navy shadow-sm" : "text-slate-400 hover:text-navy"
                }`}
              >
                <Video className="w-4 h-4" /> Videos
              </button>
            </div>
          </div>
        </div>

        <AnimatePresence mode="wait">
          {loading ? (
            <motion.div key="loader" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[1,2,3,4,5,6].map(i => <div key={i} className="h-64 bg-white rounded-[2.5rem] animate-pulse border border-navy/5"></div>)}
            </motion.div>
          ) : (
            <motion.div key={tab} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {Array.isArray(filteredData) && filteredData.map((item) => (
                <div key={item.id} className="bg-white p-8 rounded-[2.5rem] border border-navy/5 shadow-sm hover:border-gold/30 transition-all flex flex-col group relative overflow-hidden">
                   <div className="flex items-center justify-between mb-6">
                      <div className="px-4 py-1.5 bg-gold/10 text-gold text-[10px] font-black uppercase tracking-widest rounded-xl">
                        {item.subject_name}
                      </div>
                      <div className="w-8 h-8 bg-navy/5 rounded-full flex items-center justify-center text-navy/20">
                         {tab === 'notes' ? <FileText className="w-4 h-4" /> : <Video className="w-4 h-4" />}
                      </div>
                   </div>

                   <h4 className="text-xl font-black text-navy mb-3 group-hover:text-gold transition-colors">{item.title}</h4>
                   <p className="text-slate-400 text-sm font-medium line-clamp-3 mb-10 leading-relaxed italic">
                      {item.content || item.description || "No description provided."}
                   </p>
                   
                   <div className="mt-auto pt-6 border-t border-navy/5 flex items-center justify-between">
                      <div className="flex flex-col">
                         <span className="text-[10px] font-black text-slate-300 uppercase tracking-[0.15em]">Instructor</span>
                         <span className="text-xs font-bold text-navy">{item.teacher_name}</span>
                      </div>
                      
                      {tab === 'notes' ? (
                        <a href={item.file} target="_blank" className="w-12 h-12 bg-navy text-white rounded-2xl flex items-center justify-center hover:bg-gold transition-all shadow-xl shadow-navy/10 active:scale-90">
                           <Download className="w-5 h-5" />
                        </a>
                      ) : (
                        <a href={item.video_url} target="_blank" className="w-12 h-12 bg-red-500 text-white rounded-2xl flex items-center justify-center hover:bg-navy transition-all shadow-xl shadow-red-500/20 active:scale-90">
                           <Play className="w-5 h-5 fill-current" />
                        </a>
                      )}
                   </div>

                   {/* Progress Decoration */}
                   <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-100 transition-opacity">
                      <div className="w-1 h-1 bg-gold rounded-full animate-ping"></div>
                   </div>
                </div>
              ))}

              {!filteredData.length && (
                <div className="col-span-full py-32 text-center bg-white rounded-[3rem] border-2 border-dashed border-navy/5">
                  <div className="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-6">
                     <BookOpen className="w-10 h-10 text-slate-200" />
                  </div>
                  <p className="text-slate-400 font-bold italic tracking-wide uppercase text-xs">No {tab} found matching your criteria.</p>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </DashboardLayout>
  );
}
