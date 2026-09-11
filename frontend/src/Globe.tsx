import {useMemo,useRef,useState} from 'react';
import {geoContains,geoGraticule10,geoOrthographic,geoPath} from 'd3-geo';
import {feature} from 'topojson-client';
import world from 'world-atlas/countries-110m.json';
import {Minus,Plus,RotateCcw,LockKeyhole} from 'lucide-react';
import {countries} from './api';
const features=(feature(world as any,world.objects.countries as any) as any).features;
const codes:Record<string,string>={'076':'BR','840':'US','156':'CN','643':'RU'};
export function Globe({selected,toggle}:{selected:string[];toggle:(code:string)=>void}){
 const [rotation,setRotation]=useState<[number,number,number]>([55,-16,0]);
 const [zoom,setZoom]=useState(1);
 const [hover,setHover]=useState('Arraste para explorar o globo');
 const drag=useRef<{x:number;y:number;rotation:[number,number,number];moved:boolean}|null>(null);
 const moved=useRef(false);
 const projection=useMemo(()=>geoOrthographic().translate([230,207]).scale(180*zoom).rotate(rotation).clipAngle(90),[rotation,zoom]);
 const path=geoPath(projection);
 return <div className="globe-wrap">
   <svg className="globe" viewBox="0 0 460 414" role="group" aria-label="Globo interativo. Arraste para girar. Use também a lista de países ao lado." tabIndex={0}
    onKeyDown={e=>{if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)){e.preventDefault();setRotation(([x,y,z])=>[x+(e.key==='ArrowLeft'?-15:e.key==='ArrowRight'?15:0),Math.max(-80,Math.min(80,y+(e.key==='ArrowUp'?10:e.key==='ArrowDown'?-10:0))),z]);}}}
    onPointerDown={e=>{drag.current={x:e.clientX,y:e.clientY,rotation,moved:false};moved.current=false;e.currentTarget.setPointerCapture(e.pointerId);}}
    onPointerMove={e=>{const d=drag.current;if(d){const dx=e.clientX-d.x,dy=e.clientY-d.y;if(Math.abs(dx)+Math.abs(dy)>5){d.moved=true;moved.current=true;setRotation([d.rotation[0]+dx*.35,Math.max(-80,Math.min(80,d.rotation[1]-dy*.35)),0]);}}}}
    onPointerUp={e=>{if(drag.current&&!drag.current.moved){const pt=e.currentTarget.createSVGPoint();pt.x=e.clientX;pt.y=e.clientY;const local=pt.matrixTransform(e.currentTarget.getScreenCTM()!.inverse());const geo=projection.invert?.([local.x,local.y]);if(geo&&Math.hypot(local.x-230,local.y-207)<=180*zoom){const hit=features.find((f:any)=>geoContains(f,geo));if(hit){const code=codes[String(hit.id).padStart(3,'0')];if(code){toggle(code);setHover(countries[code]);}else setHover(`🔒 ${hit.properties.name} · fora do piloto`);}}}drag.current=null;e.currentTarget.releasePointerCapture(e.pointerId);}}
    onPointerCancel={()=>{drag.current=null;}}>
     <defs><radialGradient id="ocean" cx="35%" cy="26%" r="80%"><stop offset="0%" stopColor="#fcfefa"/><stop offset="70%" stopColor="#e4ede1"/><stop offset="100%" stopColor="#c1d3bf"/></radialGradient><filter id="shadow"><feDropShadow dx="0" dy="12" stdDeviation="13" floodColor="#597253" floodOpacity=".14"/></filter></defs>
     <ellipse cx="230" cy="398" rx="132" ry="7" fill="#cbd6c5" opacity=".3"/>
     <path d={path({type:'Sphere'})||''} fill="url(#ocean)" stroke="#c7d5c2" filter="url(#shadow)"/>
     <path d={path(geoGraticule10())||''} fill="none" stroke="#bccdb6" strokeWidth=".45" opacity=".55"/>
     {features.map((f:any,index:number)=>{const code=codes[String(f.id).padStart(3,'0')];const active=selected.includes(code);return <path key={String(f.id)+index} data-country={code||'locked'} d={path(f)||''} fill={code?(active?'#467756':'#88af8d'):'#dae0d4'} stroke={active?'#1c4128':'#f8faf4'} strokeWidth={active?1.3:.65} strokeDasharray={active?'3 1.3':undefined} className={code?'country-available':'country-locked'} onPointerEnter={()=>setHover(code?`${countries[code]} · ${active?'selecionado':'disponível'}`:`🔒 ${f.properties.name} · fora do piloto`)}><title>{code?countries[code]:f.properties.name}{code?(active?' — selecionado':' — disponível'):' — bloqueado neste piloto'}</title></path>})}
   </svg>
   <div className="globe-toolbar"><div className="segments"><button type="button" onClick={()=>setRotation([55,-16,0])}>Américas</button><button type="button" onClick={()=>setRotation([-105,-25,0])}>Ásia</button></div><div className="zoom"><button aria-label="Diminuir globo" onClick={()=>setZoom(z=>Math.max(.8,z-.1))}><Minus size={14}/></button><button aria-label="Aumentar globo" onClick={()=>setZoom(z=>Math.min(1.25,z+.1))}><Plus size={14}/></button><button aria-label="Restaurar globo" onClick={()=>{setRotation([55,-16,0]);setZoom(1);}}><RotateCcw size={14}/></button></div></div>
   <div className="globe-caption" aria-live="polite">{hover}</div>
   <span className="map-note"><LockKeyhole size={11}/> Demais países ainda não disponíveis · fronteiras ilustrativas</span>
 </div>
}
