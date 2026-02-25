import React, { useEffect, useState, useMemo } from 'react';
import { adminService, type Produto, type ProdutoInput, type Oferta } from '../services/adminService';
import { 
  Plus, Search, Edit2, Trash2, Package, 
  BarChart3, X, Save, Loader2, Flame 
} from 'lucide-react';

const AdminPanel: React.FC = () => {
  // Estados principais
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [ofertas, setOfertas] = useState<Oferta[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Estados de UI
  const [filter, setFilter] = useState('');
  const [form, setForm] = useState<ProdutoInput>({ nome: '', preco: 0, quantidade_estoque: 0 });
  const [editId, setEditId] = useState<number | null>(null);

  // Carregar dados iniciais (Produtos e Ofertas em paralelo)
  const carregarDados = async () => {
    try {
      const [resProd, resOfer] = await Promise.all([
        adminService.listarProdutos(),
        adminService.listarOfertas()
      ]);
      setProdutos(resProd.data);
      setOfertas(resOfer.data);
    } catch (error) {
      console.error("Erro ao sincronizar dados com o servidor");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { carregarDados(); }, []);

  // Filtro de busca em tempo real
  const produtosFiltrados = useMemo(() => {
    return produtos.filter(p => p.nome.toLowerCase().includes(filter.toLowerCase()));
  }, [produtos, filter]);

  // Estatística rápida de unidades totais
  const totalUnidades = produtos.reduce((acc, p) => acc + p.quantidade_estoque, 0);

  // Lógica de Salvar Produto (Create/Update)
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editId) {
        await adminService.editarProduto(editId, form);
      } else {
        await adminService.criarProduto(form);
      }
      setForm({ nome: '', preco: 0, quantidade_estoque: 0 });
      setEditId(null);
      carregarDados();
    } catch (error) {
      alert("Erro ao processar operação no banco de dados.");
    }
  };

  // Lógica de Excluir Produto
  const handleExcluir = async (id: number) => {
    if (confirm("Deseja remover este item permanentemente?")) {
      await adminService.excluirProduto(id);
      carregarDados();
    }
  };

  // Gerenciamento Dinâmico de Ofertas (Toggle)
  const handleToggleOferta = async (produto: Produto) => {
    const ofertaExistente = ofertas.find(o => o.produto_id === produto.id);

    if (ofertaExistente) {
      if (confirm(`Remover promoção de ${produto.nome}?`)) {
        await adminService.excluirOferta(ofertaExistente.id);
        carregarDados();
      }
    } else {
      const novoPreco = prompt(`Qual o preço de oferta para ${produto.nome}? (Original: R$ ${produto.preco.toFixed(2)})`);
      
      if (novoPreco && !isNaN(Number(novoPreco))) {
        const precoNum = Number(novoPreco);
        if (precoNum >= produto.preco) {
          alert("Atenção: O preço de oferta deve ser menor que o preço original.");
          return;
        }
        try {
          await adminService.criarOferta(produto.id, precoNum);
          carregarDados();
        } catch (error: any) {
          alert(error.response?.data?.detail || "Erro ao criar oferta");
        }
      }
    }
  };

  if (loading && produtos.length === 0) {
    return (
      <div className="flex h-screen w-full items-center justify-center bg-slate-50">
        <Loader2 className="h-10 w-10 animate-spin text-emerald-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-8 font-sans text-slate-900">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header com Estatísticas */}
        <header className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight text-slate-800">
              Painel <span className="text-emerald-600">Administrativo</span>
            </h1>
            <p className="text-slate-500 italic">Controle de estoque e promoções da Frutas & Cia.</p>
          </div>
          <div className="flex items-center gap-2 text-sm font-medium text-slate-500 bg-white p-2 rounded-lg shadow-sm border border-slate-200">
             <span className="flex items-center gap-1 px-3 border-r border-slate-200">
                <Package size={16} className="text-emerald-500" /> {produtos.length} Produtos
             </span>
             <span className="flex items-center gap-1 px-3">
                <BarChart3 size={16} className="text-blue-500" /> {totalUnidades} no Estoque
             </span>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Coluna do Formulário (Lado Esquerdo) */}
          <div className="lg:col-span-4">
            <div className="bg-white p-6 rounded-2xl shadow-md border border-slate-200 sticky top-24">
              <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                {editId ? <Edit2 size={20} className="text-blue-500" /> : <Plus size={20} className="text-emerald-500" />}
                {editId ? 'Editar Item' : 'Cadastrar Fruta'}
              </h2>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold mb-1 text-slate-700">Nome da Fruta</label>
                  <input 
                    value={form.nome} 
                    onChange={e => setForm({...form, nome: e.target.value})} 
                    className="w-full px-4 py-2 rounded-xl border border-slate-200 focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                    placeholder="Ex: Laranja Bahia"
                    required 
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold mb-1 text-slate-700">Preço (R$)</label>
                    <input 
                      type="number" step="0.01" 
                      value={form.preco} 
                      onChange={e => setForm({...form, preco: Number(e.target.value)})} 
                      className="w-full px-4 py-2 rounded-xl border border-slate-200 focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                      required 
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold mb-1 text-slate-700">Estoque (Un)</label>
                    <input 
                      type="number" 
                      value={form.quantidade_estoque} 
                      onChange={e => setForm({...form, quantidade_estoque: Number(e.target.value)})} 
                      className="w-full px-4 py-2 rounded-xl border border-slate-200 focus:ring-2 focus:ring-emerald-500 outline-none transition-all"
                      required 
                    />
                  </div>
                </div>

                <div className="flex gap-2 pt-2">
                  <button 
                    type="submit"
                    className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2.5 rounded-xl transition-colors flex items-center justify-center gap-2"
                  >
                    <Save size={18} />
                    {editId ? 'Salvar' : 'Cadastrar'}
                  </button>
                  {editId && (
                    <button 
                      type="button"
                      onClick={() => {setEditId(null); setForm({nome:'', preco:0, quantidade_estoque:0})}}
                      className="bg-slate-100 hover:bg-slate-200 text-slate-600 p-2.5 rounded-xl transition-colors"
                    >
                      <X size={20} />
                    </button>
                  )}
                </div>
              </form>
            </div>
          </div>

          {/* Coluna da Tabela (Lado Direito) */}
          <div className="lg:col-span-8 space-y-4">
            {/* Campo de Pesquisa */}
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
              <input 
                type="text"
                placeholder="Filtrar produtos por nome..."
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="w-full pl-12 pr-4 py-3 rounded-2xl border border-slate-200 bg-white shadow-sm focus:ring-2 focus:ring-emerald-500 outline-none"
              />
            </div>

            {/* Tabela de Produtos */}
            <div className="bg-white rounded-2xl shadow-md border border-slate-200 overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead className="bg-slate-50 border-b border-slate-100">
                    <tr>
                      <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-slate-500">Produto</th>
                      <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-slate-500 text-center">Qtd</th>
                      <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-slate-500">Preço Atual</th>
                      <th className="px-6 py-4 text-xs font-bold uppercase tracking-wider text-slate-500 text-right">Gerenciar</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {produtosFiltrados.map(p => {
                      const oferta = ofertas.find(o => o.produto_id === p.id);
                      
                      return (
                        <tr key={p.id} className="hover:bg-slate-50/80 transition-colors group">
                          <td className="px-6 py-4">
                            <div className="flex flex-col">
                              <span className="font-semibold text-slate-700">{p.nome}</span>
                              {oferta && (
                                <span className="text-[10px] font-black text-orange-500 flex items-center gap-0.5">
                                  <Flame size={10} fill="currentColor" /> EM OFERTA
                                </span>
                              )}
                            </div>
                          </td>
                          <td className="px-6 py-4 text-center">
                            <span className={`px-2.5 py-1 rounded-full text-xs font-bold ${
                              p.quantidade_estoque < 10 ? 'bg-amber-100 text-amber-600' : 'bg-slate-100 text-slate-600'
                            }`}>
                              {p.quantidade_estoque}
                            </span>
                          </td>
                          <td className="px-6 py-4 font-medium">
                            {oferta ? (
                              <div className="flex flex-col">
                                <span className="text-orange-600 font-bold">R$ {oferta.preco_oferta.toFixed(2)}</span>
                                <span className="text-[10px] text-slate-400 line-through">R$ {p.preco.toFixed(2)}</span>
                              </div>
                            ) : (
                              <span className="text-slate-600">R$ {p.preco.toFixed(2)}</span>
                            )}
                          </td>
                          <td className="px-6 py-4 text-right">
                            <div className="flex justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                              <button 
                                onClick={() => handleToggleOferta(p)}
                                className={`p-2 rounded-lg transition-colors ${oferta ? 'text-orange-600 bg-orange-50' : 'text-slate-400 hover:bg-slate-100'}`}
                                title={oferta ? "Remover Oferta" : "Colocar em Oferta"}
                              >
                                <Flame size={18} fill={oferta ? "currentColor" : "none"} />
                              </button>
                              <button 
                                onClick={() => { setForm(p); setEditId(p.id); window.scrollTo({top: 0, behavior: 'smooth'}); }}
                                className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                              >
                                <Edit2 size={18} />
                              </button>
                              <button 
                                onClick={() => handleExcluir(p.id)}
                                className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                              >
                                <Trash2 size={18} />
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;