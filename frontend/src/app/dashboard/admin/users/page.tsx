"use client";

import { useEffect, useState } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import DataTable from "@/components/DataTable";
import api, { usersAPI } from "@/lib/api";
import { UserCheck, ShieldCheck, Mail, ShieldAlert } from "lucide-react";
import { useToastStore } from "@/store/useToastStore";

export default function AdminUsers() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const addToast = useToastStore(s => s.addToast);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const res = await usersAPI.list();
      setData(res.data.data);
    } catch {
      addToast("Failed to sync system registry", "error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleApprove = async (id: number) => {
    try {
      await usersAPI.approve(id);
      addToast("User authorization successful.");
      fetchUsers();
    } catch {
      addToast("Authorization failed.", "error");
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-10 pb-20">
        <div>
          <h1 className="text-4xl font-black text-navy tracking-tight">System Registry</h1>
          <p className="text-slate-500 font-medium mt-1">Manage and authorize school personnel accounts.</p>
        </div>

        <DataTable 
          isLoading={loading}
          data={data}
          columns={[
            { key: "username", header: "Identity", render: (v, row) => (
              <div className="flex items-center gap-3">
                 <div className="w-8 h-8 bg-navy rounded-lg flex items-center justify-center text-gold text-[10px] font-black">{(v?.[0] || "?").toUpperCase()}</div>
                 <div>
                    <div className="font-bold text-navy">{v}</div>
                    <div className="text-[10px] text-slate-400 font-medium tracking-wide">ID: #{row.id}</div>
                 </div>
              </div>
            )},
            { key: "email", header: "Email Address" },
            { key: "role", header: "System Role", render: r => (
              <span className={`px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest ${
                r === 'ADMIN' ? 'bg-navy text-gold shadow-lg shadow-navy/10' : 
                r === 'TEACHER' ? 'bg-indigo-100 text-indigo-600' : 
                'bg-slate-100 text-slate-500'
              }`}>
                {r}
              </span>
            )},
            { key: "is_approved", header: "Status", render: a => (
               <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${a ? "bg-emerald-500 animate-pulse" : "bg-amber-400"}`}></div>
                  <span className={`text-[10px] font-black uppercase tracking-widest ${a ? "text-emerald-600" : "text-amber-600"}`}>
                    {a ? "Authorized" : "Pending"}
                  </span>
               </div>
            )},
            { key: "actions", header: "Control", render: (_, row: any) => (
              !row.is_approved && (
                <button 
                  onClick={() => handleApprove(row.id)}
                  className="flex items-center gap-2 bg-emerald-500 text-white px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-emerald-600 transition-all shadow-lg shadow-emerald-500/20 active:scale-95"
                >
                  <UserCheck className="w-3.5 h-3.5" />
                  Grant Access
                </button>
              )
            )}
          ]}
        />
      </div>
    </DashboardLayout>
  );
}
