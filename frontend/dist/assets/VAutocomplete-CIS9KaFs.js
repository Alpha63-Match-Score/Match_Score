import{m as Se,u as Ce,b as xe,c as Me,d as Ie,a as pe}from"./VSelect-BpGEebQz.js";import{Q as re,r as R,J as C,B as H,ai as Ae,ar as q,aC as Pe,X as Ke,aD as _e,aE as De,Z as Le,at as Re,a5 as B,$ as Y,aF as Oe,aG as Ee,aH as Te,m as J,ag as te,aI as Be,a9 as Ne,L as ae,b as i,F as Q,s as L,aJ as je,O as ue,q as Ue,v as ne,aK as ze,ac as He,x as Je,aL as Qe,ad as $e,aM as Ge,aN as oe}from"./index-DD0chK9m.js";const We=(e,c,t)=>e==null||c==null?-1:e.toString().toLocaleLowerCase().indexOf(c.toString().toLocaleLowerCase()),Xe=re({customFilter:Function,customKeyFilter:Object,filterKeys:[Array,String],filterMode:{type:String,default:"intersection"},noFilter:Boolean},"filter");function Ze(e,c,t){var I;const S=[],m=(t==null?void 0:t.default)??We,g=t!=null&&t.filterKeys?q(t.filterKeys):!1,y=Object.keys((t==null?void 0:t.customKeyFilter)??{}).length;if(!(e!=null&&e.length))return S;e:for(let F=0;F<e.length;F++){const[w,p=w]=q(e[F]),r={},o={};let V=-1;if((c||y>0)&&!(t!=null&&t.noFilter)){if(typeof w=="object"){const O=g||Object.keys(p);for(const x of O){const N=Pe(p,x),E=(I=t==null?void 0:t.customKeyFilter)==null?void 0:I[x];if(V=E?E(N,c,w):m(N,c,w),V!==-1&&V!==!1)E?r[x]=V:o[x]=V;else if((t==null?void 0:t.filterMode)==="every")continue e}}else V=m(w,c,w),V!==-1&&V!==!1&&(o.title=V);const A=Object.keys(o).length,P=Object.keys(r).length;if(!A&&!P||(t==null?void 0:t.filterMode)==="union"&&P!==y&&!A||(t==null?void 0:t.filterMode)==="intersection"&&(P!==y||!A))continue}S.push({index:F,matches:{...o,...r}})}return S}function Ye(e,c,t,S){const m=R([]),g=R(new Map),y=C(()=>H(c));Ae(()=>{const F=typeof t=="function"?t():H(t),w=typeof F!="string"&&typeof F!="number"?"":String(F),p=Ze(y.value,w,{customKeyFilter:{...e.customKeyFilter,...H(S==null?void 0:S.customKeyFilter)},default:e.customFilter,filterKeys:e.filterKeys,filterMode:e.filterMode,noFilter:e.noFilter}),r=H(c),o=[],V=new Map;p.forEach(A=>{let{index:P,matches:O}=A;const x=r[P];o.push(x),V.set(x.value,O)}),m.value=o,g.value=V});function I(F){return g.value.get(F.value)}return{filteredItems:m,filteredMatches:g,getMatches:I}}function qe(e,c,t){if(c==null)return e;if(Array.isArray(c))throw new Error("Multiple matches is not implemented");return typeof c=="number"&&~c?i(Q,null,[i("span",{class:"v-autocomplete__unmask"},[e.substr(0,c)]),i("span",{class:"v-autocomplete__mask"},[e.substr(c,t)]),i("span",{class:"v-autocomplete__unmask"},[e.substr(c+t)])]):e}const el=re({autoSelectFirst:{type:[Boolean,String]},clearOnSelect:Boolean,search:String,...Xe({filterKeys:["title"]}),...Se(),...Ke(_e({modelValue:null,role:"combobox"}),["validationValue","dirty","appendInnerIcon"]),...De({transition:!1})},"VAutocomplete"),al=Le()({name:"VAutocomplete",props:el(),emits:{"update:focused":e=>!0,"update:search":e=>!0,"update:modelValue":e=>!0,"update:menu":e=>!0},setup(e,c){let{slots:t}=c;const{t:S}=Re(),m=R(),g=B(!1),y=B(!0),I=B(!1),F=R(),w=R(),p=Y(e,"menu"),r=C({get:()=>p.value,set:l=>{var a;p.value&&!l&&((a=F.value)!=null&&a.ΨopenChildren.size)||(p.value=l)}}),o=B(-1),V=C(()=>{var l;return(l=m.value)==null?void 0:l.color}),A=C(()=>r.value?e.closeText:e.openText),{items:P,transformIn:O,transformOut:x}=Oe(e),{textColorClasses:N,textColorStyles:E}=Ee(V),f=Y(e,"search",""),n=Y(e,"modelValue",[],l=>O(l===null?[null]:q(l)),l=>{const a=x(l);return e.multiple?a:a[0]??null}),ie=C(()=>typeof e.counterValue=="function"?e.counterValue(n.value):typeof e.counterValue=="number"?e.counterValue:n.value.length),D=Te(),{filteredItems:$,getMatches:se}=Ye(e,P,()=>y.value?"":f.value),M=C(()=>e.hideSelected?$.value.filter(l=>!n.value.some(a=>a.value===l.value)):$.value),j=C(()=>!!(e.chips||t.chip)),T=C(()=>j.value||!!t.selection),ce=C(()=>n.value.map(l=>l.props.value)),G=C(()=>{var a;return(e.autoSelectFirst===!0||e.autoSelectFirst==="exact"&&f.value===((a=M.value[0])==null?void 0:a.title))&&M.value.length>0&&!y.value&&!I.value}),W=C(()=>e.hideNoData&&!M.value.length||e.readonly||(D==null?void 0:D.isReadonly.value)),X=R(),ve=Ce(X,m);function fe(l){e.openOnClear&&(r.value=!0),f.value=""}function de(){W.value||(r.value=!0)}function me(l){W.value||(g.value&&(l.preventDefault(),l.stopPropagation()),r.value=!r.value)}function he(l){var a;Ge(l)&&((a=m.value)==null||a.focus())}function ge(l){var u,s,k;if(e.readonly||D!=null&&D.isReadonly.value)return;const a=m.value.selectionStart,v=n.value.length;if((o.value>-1||["Enter","ArrowDown","ArrowUp"].includes(l.key))&&l.preventDefault(),["Enter","ArrowDown"].includes(l.key)&&(r.value=!0),["Escape"].includes(l.key)&&(r.value=!1),G.value&&["Enter","Tab"].includes(l.key)&&!n.value.some(d=>{let{value:h}=d;return h===M.value[0].value})&&K(M.value[0]),l.key==="ArrowDown"&&G.value&&((u=X.value)==null||u.focus("next")),["Backspace","Delete"].includes(l.key)){if(!e.multiple&&T.value&&n.value.length>0&&!f.value)return K(n.value[0],!1);if(~o.value){const d=o.value;K(n.value[o.value],!1),o.value=d>=v-1?v-2:d}else l.key==="Backspace"&&!f.value&&(o.value=v-1)}if(e.multiple){if(l.key==="ArrowLeft"){if(o.value<0&&a>0)return;const d=o.value>-1?o.value-1:v-1;n.value[d]?o.value=d:(o.value=-1,m.value.setSelectionRange((s=f.value)==null?void 0:s.length,(k=f.value)==null?void 0:k.length))}if(l.key==="ArrowRight"){if(o.value<0)return;const d=o.value+1;n.value[d]?o.value=d:(o.value=-1,m.value.setSelectionRange(0,0))}}}function ye(l){if(oe(m.value,":autofill")||oe(m.value,":-webkit-autofill")){const a=P.value.find(v=>v.title===l.target.value);a&&K(a)}}function Ve(){var l;e.eager&&((l=w.value)==null||l.calculateVisibleItems())}function Fe(){var l;g.value&&(y.value=!0,(l=m.value)==null||l.focus())}function ke(l){g.value=!0,setTimeout(()=>{I.value=!0})}function be(l){I.value=!1}function we(l){(l==null||l===""&&!e.multiple&&!T.value)&&(n.value=[])}const Z=B(!1);function K(l){let a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!0;if(!(!l||l.props.disabled))if(e.multiple){const v=n.value.findIndex(s=>e.valueComparator(s.value,l.value)),u=a??!~v;if(~v){const s=u?[...n.value,l]:[...n.value];s.splice(v,1),n.value=s}else u&&(n.value=[...n.value,l]);e.clearOnSelect&&(f.value="")}else{const v=a!==!1;n.value=v?[l]:[],f.value=v&&!T.value?l.title:"",te(()=>{r.value=!1,y.value=!0})}}return J(g,(l,a)=>{var v;l!==a&&(l?(Z.value=!0,f.value=e.multiple||T.value?"":String(((v=n.value.at(-1))==null?void 0:v.props.title)??""),y.value=!0,te(()=>Z.value=!1)):(!e.multiple&&f.value==null&&(n.value=[]),r.value=!1,n.value.some(u=>{let{title:s}=u;return s===f.value})||(f.value=""),o.value=-1))}),J(f,l=>{!g.value||Z.value||(l&&(r.value=!0),y.value=!l)}),J(r,()=>{if(!e.hideSelected&&r.value&&n.value.length){const l=M.value.findIndex(a=>n.value.some(v=>a.value===v.value));Be&&window.requestAnimationFrame(()=>{var a;l>=0&&((a=w.value)==null||a.scrollToIndex(l))})}}),J(()=>e.items,(l,a)=>{r.value||g.value&&!a.length&&l.length&&(r.value=!0)}),Ne(()=>{const l=!!(!e.hideNoData||M.value.length||t["prepend-item"]||t["append-item"]||t["no-data"]),a=n.value.length>0,v=ae.filterProps(e);return i(ae,L({ref:m},v,{modelValue:f.value,"onUpdate:modelValue":[u=>f.value=u,we],focused:g.value,"onUpdate:focused":u=>g.value=u,validationValue:n.externalValue,counterValue:ie.value,dirty:a,onChange:ye,class:["v-autocomplete",`v-autocomplete--${e.multiple?"multiple":"single"}`,{"v-autocomplete--active-menu":r.value,"v-autocomplete--chips":!!e.chips,"v-autocomplete--selection-slot":!!T.value,"v-autocomplete--selecting-index":o.value>-1},e.class],style:e.style,readonly:e.readonly,placeholder:a?void 0:e.placeholder,"onClick:clear":fe,"onMousedown:control":de,onKeydown:ge}),{...t,default:()=>i(Q,null,[i(xe,L({ref:F,modelValue:r.value,"onUpdate:modelValue":u=>r.value=u,activator:"parent",contentClass:"v-autocomplete__content",disabled:W.value,eager:e.eager,maxHeight:310,openOnClick:!1,closeOnContentClick:!1,transition:e.transition,onAfterEnter:Ve,onAfterLeave:Fe},e.menuProps),{default:()=>[l&&i(je,L({ref:X,selected:ce.value,selectStrategy:e.multiple?"independent":"single-independent",onMousedown:u=>u.preventDefault(),onKeydown:he,onFocusin:ke,onFocusout:be,tabindex:"-1","aria-live":"polite",color:e.itemColor??e.color},ve,e.listProps),{default:()=>{var u,s,k;return[(u=t["prepend-item"])==null?void 0:u.call(t),!M.value.length&&!e.hideNoData&&(((s=t["no-data"])==null?void 0:s.call(t))??i(ue,{title:S(e.noDataText)},null)),i(Me,{ref:w,renderless:!0,items:M.value},{default:d=>{var le;let{item:h,index:_,itemRef:b}=d;const ee=L(h.props,{ref:b,key:_,active:G.value&&_===0?!0:void 0,onClick:()=>K(h,null)});return((le=t.item)==null?void 0:le.call(t,{item:h,index:_,props:ee}))??i(ue,L(ee,{role:"option"}),{prepend:U=>{let{isSelected:z}=U;return i(Q,null,[e.multiple&&!e.hideSelected?i(Ie,{key:h.value,modelValue:z,ripple:!1,tabindex:"-1"},null):void 0,h.props.prependAvatar&&i(Ue,{image:h.props.prependAvatar},null),h.props.prependIcon&&i(ne,{icon:h.props.prependIcon},null)])},title:()=>{var U,z;return y.value?h.title:qe(h.title,(U=se(h))==null?void 0:U.title,((z=f.value)==null?void 0:z.length)??0)}})}}),(k=t["append-item"])==null?void 0:k.call(t)]}})]}),n.value.map((u,s)=>{function k(b){b.stopPropagation(),b.preventDefault(),K(u,!1)}const d={"onClick:close":k,onKeydown(b){b.key!=="Enter"&&b.key!==" "||(b.preventDefault(),b.stopPropagation(),k(b))},onMousedown(b){b.preventDefault(),b.stopPropagation()},modelValue:!0,"onUpdate:modelValue":void 0},h=j.value?!!t.chip:!!t.selection,_=h?ze(j.value?t.chip({item:u,index:s,props:d}):t.selection({item:u,index:s})):void 0;if(!(h&&!_))return i("div",{key:u.value,class:["v-autocomplete__selection",s===o.value&&["v-autocomplete__selection--selected",N.value]],style:s===o.value?E.value:{}},[j.value?t.chip?i(He,{key:"chip-defaults",defaults:{VChip:{closable:e.closableChips,size:"small",text:u.title}}},{default:()=>[_]}):i(pe,L({key:"chip",closable:e.closableChips,size:"small",text:u.title,disabled:u.props.disabled},d),null):_??i("span",{class:"v-autocomplete__selection-text"},[u.title,e.multiple&&s<n.value.length-1&&i("span",{class:"v-autocomplete__selection-comma"},[Je(",")])])])})]),"append-inner":function(){var d;for(var u=arguments.length,s=new Array(u),k=0;k<u;k++)s[k]=arguments[k];return i(Q,null,[(d=t["append-inner"])==null?void 0:d.call(t,...s),e.menuIcon?i(ne,{class:"v-autocomplete__menu-icon",icon:e.menuIcon,onMousedown:me,onClick:Qe,"aria-label":S(A.value),title:S(A.value),tabindex:"-1"},null):void 0])}})}),$e({isFocused:g,isPristine:y,menu:r,search:f,filteredItems:$,select:K},m)}});export{al as V};
