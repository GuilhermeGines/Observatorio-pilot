export let token='';
export async function api<T=any>(path:string,method='GET',body?:unknown):Promise<T>{
  const response=await fetch('/api'+path,{method,headers:{'Content-Type':'application/json','X-Observatorio-Token':token},body:body===undefined?undefined:JSON.stringify(body)});
  if(!response.ok){const error=await response.json().catch(()=>({detail:'Falha de conexão com o aplicativo local.'}));throw new Error(typeof error.detail==='string'?error.detail:'Verifique os campos e o intervalo de datas.');}
  return response.json();
}
export async function initialize(){const result=await api('/session');token=result.token;return result;}
export const countries:Record<string,string>={BR:'Brasil',US:'Estados Unidos',CN:'China',RU:'Rússia'};
export const topics:Record<string,string>={geopolitica:'Geopolítica',politica:'Política nacional',ciencia:'Ciência',fisica:'Física',astronomia:'Astronomia',tecnologia:'Tecnologia e IA',economia:'Economia e comércio',clima:'Energia e clima',defesa:'Defesa e segurança',saude:'Saúde e pesquisa médica'};
export const statusNames:Record<string,string>={nao_testado:'Ainda não testada',disponivel:'Texto recuperado',parcial:'Cobertura parcial',indisponivel:'Indisponível',desatualizado:'Canal desatualizado',desativada:'Desativada',acervo:'Acervo local'};
export function displayDate(value:string|null,editorial=false){if(!value)return 'Não verificada';if(value.length>10&&!editorial)return new Date(value).toLocaleDateString('pt-BR');const [year,month,day]=value.slice(0,10).split('-');return `${day}/${month}/${year}`;}
export function dayOffset(offset:number){const date=new Date();date.setDate(date.getDate()+offset);return `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;}
export type Doc={revision_id:number;document_id:number;source_id:string;source_name:string;title:string;text:string;country:string;published_at:string|null;collected_at:string;url:string;access:string;access_note:string;author:string;genre:string;origin:string;topics:string[];study_links:{url:string;label:string;status:string}[];affiliation:string};
export type Evidence={revision_id:number;quote:string};
