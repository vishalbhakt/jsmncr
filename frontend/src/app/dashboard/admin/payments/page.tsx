"use client";

import { useEffect, useState } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import DataTable from "@/components/DataTable";
import api, { paymentsAPI, studentsAPI } from "@/lib/api";
import { 
  CreditCard, 
  Search, 
  BarChart3, 
  TrendingUp, 
  Download,
  AlertCircle,
  Plus,
  Trash2,
  CheckCircle,
  Clock,
  X
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useToastStore } from "@/store/useToastStore";

export default function AdminPayments() {
  const [data, setData] = useState<any[]>([]);
  const [students, setStudents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [isAdding, setIsAdding] = useState(false);
  const [formData, setFormData] = useState({ student: "", amount: "", due_date: "", description: "Monthly Tuition", status: "Pending" });
  const addToast = useToastStore(s => s.addToast);

  const fetchPayments = async () => {
    setLoading(true);
    try {
      const [pRes, sRes] = await Promise.all([
        paymentsAPI.list(),
        studentsAPI.list()
      ]);
      setData(pRes.data.data);
      setStudents(sRes.data.data);
    } catch {
      addToast("Failed to sync financial ledger", "error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPayments();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await paymentsAPI.create(formData);
      addToast("Fee record created successfully!");
      setIsAdding(false);
      setFormData({ student: "", amount: "", due_date: "", description: "Monthly Tuition", status: "Pending" });
      fetchPayments();
    } catch {
      addToast("Failed to create record", "error");
    }
  };

  const handleUpdateStatus = async (id: number, status: string) => {
    try {
      await paymentsAPI.update(id, { status });
      addToast(`Payment marked as ${status}`);
      fetchPayments();
    } catch {
      addToast("Update failed", "error");
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Remove this payment record?")) return;
    try {
      await paymentsAPI.delete(id);
      setData(data.filter(p => p.id !== id));
      addToast("Record deleted.");
    } catch {
      addToast("Delete failed", "error");
    }
  };

  const totalCollected = Array.isArray(data) ? data.filter((p: any) => p.status === 'Paid').reduce((sum, p: any) => sum + parseFloat(p.amount), 0) : 0;
  const totalPending = Array.isArray(data) ? data.filter((p: any) => p.status === 'Pending').reduce((sum, p: any) => sum + parseFloat(p.amount), 0) : 0;

  const filteredData = Array.isArray(data) ? data.filter(p => 
    p.student_name.toLowerCase().includes(search.toLowerCase())
  ) : [];

  return (
    <DashboardLayout>
      <div className="space-y-10 pb-20">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <h1 className="text-4xl font-black text-navy tracking-tight">Financial Ledger</h1>
            <p className="text-slate-500 font-medium mt-1">Institutional fee management and student payment oversight.</p>
          </div>
          <div className="flex gap-4">
             <button 
              onClick={() => setIsAdding(!isAdding)}
              className="btn-gold flex items-center gap-2 shadow-xl shadow-gold/20"
             >
                {isAdding ? "Cancel" : <><Plus className="w-4 h-4" /> Add Fee Detail</>}
             </button>
             <button className="p-3 bg-white border border-navy/5 rounded-2xl shadow-sm hover:text-gold transition-all"><Download className="w-5 h-5" /></button>
          </div>
        </div>

        <AnimatePresence>
          {isAdding && (
            <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} className="bg-white p-10 rounded-[3rem] border-2 border-gold/20 shadow-2xl space-y-8">
               <h3 className="text-2xl font-black text-navy uppercase tracking-widest">New Fee Entry</h3>
               <form onSubmit={handleCreate} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <div className="space-y-2">
                     <label className="text-[10px] font-black uppercase text-slate-400 ml-1">Select Student</label>
                     <select required className="w-full bg-slate-50 border-2 border-slate-100 rounded-2xl px-5 py-4 font-bold outline-none focus:border-gold"
                        value={formData.student} onChange={e => setFormData({...formData, student: e.target.value})}>
                        <option value="">-- Choose Student --</option>
                        {Array.isArray(students) && students.map(s => <option key={s.id} value={s.id}>{s.user.first_name} {s.user.last_name} ({s.roll_number})</option>)}
                     </select>
                  </div>
                  <div className="space-y-2">
                     <label className="text-[10px] font-black uppercase text-slate-400 ml-1">Amount (₹)</label>
                     <input type="number" required className="w-full bg-slate-50 border-2 border-slate-100 rounded-2xl px-5 py-4 font-bold outline-none focus:border-gold"
                        value={formData.amount} onChange={e => setFormData({...formData, amount: e.target.value})} />
                  </div>
                  <div className="space-y-2">
                     <label className="text-[10px] font-black uppercase text-slate-400 ml-1">Due Date</label>
                     <input type="date" required className="w-full bg-slate-50 border-2 border-slate-100 rounded-2xl px-5 py-4 font-bold outline-none focus:border-gold"
                        value={formData.due_date} onChange={e => setFormData({...formData, due_date: e.target.value})} />
                  </div>
                  <div className="space-y-2">
                     <label className="text-[10px] font-black uppercase text-slate-400 ml-1">Description</label>
                     <input required className="w-full bg-slate-50 border-2 border-slate-100 rounded-2xl px-5 py-4 font-bold outline-none focus:border-gold"
                        value={formData.description} onChange={e => setFormData({...formData, description: e.target.value})} />
                  </div>
                  <button type="submit" className="lg:col-span-4 btn-primary py-5 rounded-2xl font-black uppercase tracking-widest text-xs shadow-xl shadow-navy/20">Commit Fee Record</button>
               </form>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
           <div className="bg-white p-8 rounded-[2.5rem] border border-navy/5 shadow-sm flex flex-col justify-between h-44 group hover:border-emerald-500/30 transition-all">
              <div className="text-[10px] font-black uppercase text-slate-400 tracking-widest">Total Collected</div>
              <div className="text-4xl font-black text-emerald-600">₹{totalCollected.toLocaleString()}</div>
           </div>
           <div className="bg-white p-8 rounded-[2.5rem] border border-navy/5 shadow-sm flex flex-col justify-between h-44 group hover:border-rose-500/30 transition-all">
              <div className="text-[10px] font-black uppercase text-slate-400 tracking-widest">Outstanding Dues</div>
              <div className="text-4xl font-black text-rose-500">₹{totalPending.toLocaleString()}</div>
           </div>
           <div className="bg-navy p-8 rounded-[2.5rem] shadow-xl flex flex-col justify-between h-44 relative overflow-hidden">
              <div className="relative z-10 text-[10px] font-black uppercase text-white/40 tracking-widest">Collection Rate</div>
              <div className="relative z-10 text-4xl font-black text-gold">94%</div>
              <BarChart3 className="absolute -bottom-4 -right-4 w-24 h-24 text-white/5 rotate-12" />
           </div>
        </div>

        <div className="bg-white rounded-[2.5rem] border border-navy/5 shadow-sm overflow-hidden">
           <div className="p-8 border-b border-navy/5 flex items-center justify-between">
              <div className="relative w-full max-w-xs group">
                 <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-300 group-focus-within:text-gold transition-all" />
                 <input 
                   placeholder="Filter by student name..."
                   className="w-full bg-slate-50 border-2 border-slate-100 rounded-xl pl-10 pr-4 py-2 font-bold text-xs outline-none focus:border-gold transition-all"
                   value={search}
                   onChange={e => setSearch(e.target.value)}
                 />
              </div>
           </div>

           <DataTable 
             isLoading={loading}
             data={filteredData}
             columns={[
               { key: "student_name", header: "Identity", render: (v, row) => (
                 <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-navy/5 rounded-lg flex items-center justify-center text-navy font-black text-[10px]">{v[0]}</div>
                    <div>
                       <div className="font-bold text-navy">{v}</div>
                       <div className="text-[9px] text-slate-400 font-bold uppercase tracking-wider">{row.description}</div>
                    </div>
                 </div>
               )},
               { key: "amount", header: "Value", render: v => <span className="font-black text-navy text-lg">₹{parseFloat(v).toLocaleString()}</span> },
               { key: "status", header: "Payment Status", render: s => (
                 <span className={`px-4 py-1.5 rounded-full text-[8px] font-black uppercase tracking-[0.15em] ${
                   s === 'Paid' ? "bg-emerald-500/10 text-emerald-600" : "bg-rose-500/10 text-rose-600"
                 }`}>
                   {s}
                 </span>
               )},
               { key: "due_date", header: "Deadline", render: d => <span className="text-slate-400 font-bold">{new Date(d).toLocaleDateString()}</span> },
               { key: "actions", header: "Control", render: (_, row: any) => (
                 <div className="flex gap-2">
                    {row.status === 'Pending' ? (
                      <button onClick={() => handleUpdateStatus(row.id, 'Paid')} className="p-2 bg-emerald-50 text-emerald-600 rounded-xl hover:bg-emerald-600 hover:text-white transition-all shadow-sm"><CheckCircle className="w-4 h-4" /></button>
                    ) : (
                      <button onClick={() => handleUpdateStatus(row.id, 'Pending')} className="p-2 bg-amber-50 text-amber-600 rounded-xl hover:bg-amber-600 hover:text-white transition-all shadow-sm"><Clock className="w-4 h-4" /></button>
                    )}
                    <button onClick={() => handleDelete(row.id)} className="p-2 bg-rose-50 text-rose-500 rounded-xl hover:bg-rose-600 hover:text-white transition-all shadow-sm"><Trash2 className="w-4 h-4" /></button>
                 </div>
               )}
             ]}
           />
        </div>
      </div>
    </DashboardLayout>
  );
}
