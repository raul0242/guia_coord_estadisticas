import streamlit as st
import random
import json
from datetime import datetime
from pathlib import Path

# ============================================================
# GUÍA INTERACTIVA - COORDINADOR DE ESTADÍSTICA (IMSS)
# Material Didáctico C.P. 05 - 2020
# ============================================================

st.set_page_config(
    page_title="Guía Coordinador de Estadística - IMSS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- CSS personalizado ---
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #006847 0%, #00843D 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .main-header h1 { color: white; margin: 0; font-size: 1.8rem; }
    .main-header p { color: #d4edda; margin: 0.3rem 0 0 0; font-size: 1rem; }
    .tema-card {
        background: #1a1a2e;
        border-left: 4px solid #006847;
        padding: 1rem 1.2rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.8rem;
        color: #e0e0e0;
    }
    .correct { background-color: #1b4332; color: #d4edda; padding: 1rem; border-radius: 8px; border-left: 4px solid #28a745; }
    .incorrect { background-color: #4a1520; color: #f8d7da; padding: 1rem; border-radius: 8px; border-left: 4px solid #dc3545; }
    .score-box {
        background: linear-gradient(135deg, #006847, #00843D);
        color: white; padding: 1.2rem; border-radius: 12px;
        text-align: center; font-size: 1.3rem;
    }
    .study-note {
        background: #3d2e00; border-left: 4px solid #ffc107;
        padding: 1rem; border-radius: 0 8px 8px 0; margin: 0.5rem 0;
        color: #ffe69c;
    }
    .flashcard-front {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; padding: 2rem; border-radius: 12px;
        text-align: center; min-height: 150px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.2rem; cursor: pointer;
    }
    .flashcard-back {
        background: #1a1a2e; padding: 2rem; border-radius: 12px;
        text-align: center; min-height: 150px;
        display: flex; align-items: center; justify-content: center;
        border: 2px solid #764ba2;
        color: #ffffff;
    }
    div[data-testid="stExpander"] { border: 1px solid #dee2e6; border-radius: 8px; margin-bottom: 0.5rem; }
    @media (max-width: 768px) {
        .main-header h1 { font-size: 1.3rem; }
        .main-header p { font-size: 0.85rem; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# BASE DE CONOCIMIENTO - Contenido extraído del PDF
# ============================================================

TEMAS = {
    "I. Normatividad y Marco Legal": {
        "icono": "⚖️",
        "descripcion": "Leyes, normas y lineamientos que regulan la información en salud del IMSS.",
        "subtemas": {
            "Ley General de Salud": [
                "Establece las bases del Sistema Nacional de Salud.",
                "Regula la prestación de servicios de salud y salubridad general.",
                "Art. 104: La Secretaría de Salud y los gobiernos de las entidades federativas recopilarán datos para el proceso de planeación.",
                "Art. 105: Las instituciones del SNS deberán proporcionar la información de sus actividades.",
                "Art. 107: Los establecimientos de salud llevarán sistemas de información.",
            ],
            "NOM-035-SSA3-2012 (Información en Salud)": [
                "Establece criterios y procedimientos para producir, captar, integrar, procesar, sistematizar, evaluar y divulgar la Información en Salud.",
                "Regula el Centro de Inteligencia en Salud.",
                "CLUES: Clave Única de Establecimientos de Salud.",
                "DGIS: Dirección General de Información en Salud.",
                "SEED: Subsistema Epidemiológico y Estadístico de Defunciones.",
                "SINAC: Subsistema de Información sobre Nacimientos.",
                "SINAIS: Sistema Nacional de Información en Salud.",
                "Atributos de calidad: Oportunidad, Cobertura, Integridad, Confiabilidad, Validez y Consistencia.",
                "La codificación con clasificaciones internacionales (CIE, CIF, CIE-MC) debe efectuarse a nivel de 4 dígitos.",
            ],
            "Ley General de Transparencia y Acceso a la Información Pública": [
                "Publicada en DOF el 04 de mayo de 2015.",
                "Primer ordenamiento que regula el tratamiento de datos personales en sector público federal, estatal y municipal.",
                "Bases para la elaboración de un Programa Nacional de Protección de Datos Personales.",
            ],
            "Ley Federal de Transparencia y Acceso a la Información Pública": [
                "Última reforma en DOF 26 de enero de 2017.",
                "Art. 1: Garantizar el derecho de acceso a la Información Pública en posesión de cualquier autoridad.",
                "Art. 9: Sujetos obligados a transparentar y permitir acceso a la información.",
                "Art. 10: Los sujetos obligados deben mantener actualizados sus sistemas de archivo y gestión documental.",
            ],
            "Ley Federal de Archivos": [
                "Publicada en DOF el 23 de enero de 2012.",
                "Archivo: conjunto orgánico de documentos en cualquier soporte.",
                "Archivo de concentración: documentos de consulta esporádica.",
                "Archivo de trámite: documentos de uso cotidiano.",
                "Archivo histórico: documentos de conservación permanente.",
                "Clasificación archivística: proceso de identificación y agrupación de expedientes homogéneos.",
                "Destino final: selección de expedientes cuyo plazo de conservación ha prescrito (baja o transferencia a archivo histórico).",
                "Expediente: unidad documental constituida por uno o varios documentos de archivo.",
            ],
            "MAAGTIC": [
                "Manual Administrativo de Aplicación General para las Tecnologías de la Información y la Comunicación.",
                "Emite políticas y disposiciones para la Estrategia Digital Nacional en materia de TIC.",
                "Administra la continuidad de servicios de Tecnologías de la Información y la Comunicación.",
            ],
        },
    },
    "II. Expediente Clínico y ARIMAC": {
        "icono": "🏥",
        "descripcion": "Todo sobre el Expediente Clínico, el Archivo Clínico (ARIMAC), apertura, integración, control y conservación.",
        "subtemas": {
            "El Expediente Clínico": [
                "Conjunto único de información y datos personales de un paciente.",
                "Consta de documentos escritos, gráficos, imagenológicos, electrónicos, magnéticos, etc.",
                "Es un documento médico-legal y base para la asistencia, docencia e investigación.",
                "Trasciende la relación médico-paciente.",
                "Contiene datos confidenciales.",
            ],
            "Integración del Expediente": [
                "Debe contener: Historia Clínica, Interrogatorio, Exploración Física.",
                "Resultados de estudios de laboratorio y gabinete.",
                "Diagnósticos o problemas clínicos.",
                "Plan de tratamiento.",
                "Hoja de enfermería.",
                "Cartas de consentimiento informado.",
                "Hoja de egreso voluntario.",
                "Notas de defunción y muerte fetal.",
                "Debe estar dentro de una carpeta de contención debidamente identificada.",
                "Los documentos deben ir acomodados de manera cronológica.",
            ],
            "Archivo Clínico (ARIMAC)": [
                "ARIMAC: Área de Información Médica y Archivo Clínico.",
                "Es el lugar donde se guardan los expedientes clínicos debidamente ordenados.",
                "Tipos de documentos: Documentos de archivo, Documentos de comprobación administrativa inmediata, Documentos de apoyo informativo.",
                "Etapas del procedimiento: Apertura, Integración, Control, Revisión sistemática, Depuración.",
            ],
            "Conservación y Resguardo": [
                "Los expedientes clínicos deben conservarse por un mínimo de 5 años.",
                "Formatos a conservar en Archivo Clínico: RAIS, Notas médicas, Informe Semanal, Informes mensuales.",
                "Los cuadros electrónicos se deben guardar en carpetas anuales y subcarpetas por mes.",
                "Se deben respaldar en el equipo generador y en otro equipo diferente.",
            ],
        },
    },
    "III. Sistemas de Información en Salud": {
        "icono": "💻",
        "descripcion": "Sistemas electrónicos del IMSS para captura, procesamiento y análisis de información estadística médica.",
        "subtemas": {
            "SIAIS (Sistema de Información de Atención Integral a la Salud)": [
                "Sistema para registrar las atenciones en Medicina Familiar.",
                "Genera información estadística de las consultas y actividades preventivas.",
                "Registra diariamente el formato RAIS.",
                "Transfiere consultas del SIMF al SIAIS.",
                "Genera archivos tipo texto (TXT) de subsistemas: 10, 13, 27, 31 y 32.",
            ],
            "SIMO Central (Sistema de Información Médico Operativo)": [
                "Módulos: Consulta Externa, Hospitalización y Enlace.",
                "Cada módulo tiene su Manual de Operación.",
                "Captura de formatos de consulta externa de especialidades (4-30-6 y 4-30-6P/90).",
                "Al cierre de mes genera archivos TXT de los subsistemas.",
                "Emitido por la Dirección de Innovación y Desarrollo Tecnológico (DIDT).",
            ],
            "SIMF (Sistema de Información de Medicina Familiar)": [
                "Contiene las actividades para apoyar el proceso de atenciones a derechohabientes.",
                "Proporciona información estadística de acuerdo a la CIE-10.",
                "Simplifica el proceso de captura de información al personal del ARIMAC.",
                "Interface con el SIAIS.",
            ],
            "DataMart Estadísticas Médicas": [
                "Desarrollado en 2003 por la División de Información en Salud.",
                "Implantación en enero de 2004.",
                "Opera en 35 delegaciones (CIAE) y 25 UMAE.",
                "Repositorio que almacena grandes volúmenes de datos para análisis prospectivo.",
                "Desarrollado en tecnología WEB.",
                "Módulos: Captura de Formatos, Validación SIAIS/SIMO, Envío de Información, Administrador.",
                "Subsistemas manuales: 12, 14, 15, 19, 29, 43, 46, 47, 48, 49.",
                "Subsistemas automatizados (SIAIS/SIMO): 10, 13, 27, 31, 32.",
                "Data Warehouse: Conjunto de DataMarts que mantienen las mismas características.",
            ],
            "SEED (Sistema de Mortalidad)": [
                "Subsistema Epidemiológico y Estadístico de Defunciones.",
                "Permite registrar, codificar y procesar los certificados de defunción.",
                "Genera estadísticas de mortalidad.",
            ],
        },
    },
    "IV. Vigilancia Epidemiológica": {
        "icono": "🔬",
        "descripcion": "Procesos de vigilancia, informe semanal de enfermedades y sistemas de notificación.",
        "subtemas": {
            "Informe Semanal de Enfermedades": [
                "Informe Semanal de Enfermedades Transmisibles y No Transmisibles.",
                "Se genera con el SIAIS.",
                "Archivo de enlace SUAVE con nomenclatura BAEE00SS.DBF (EE=clave del Estado, SS=número de semana).",
                "Se sube a la plataforma IBSv2 Informe Semanal.",
                "El Epidemiólogo valida la información.",
                "Los listados nominales solo se usan en el ARIMAC para corregir información.",
                "La CIAE integra la información de todas las unidades.",
            ],
            "SUIVE (Sistema Único de Información para Vigilancia Epidemiológica)": [
                "Permite la notificación de padecimientos de interés epidemiológico.",
                "Genera listados nominales de padecimientos del informe semanal.",
                "Listados nominales de padecimientos de interés epidemiológico.",
            ],
            "Resguardo de Documentos Epidemiológicos": [
                "RAIS: formato de Registro de Actividades de Atención Integral de la Salud.",
                "Notas médicas (Urgencias, Epidemiólogo, Médico Familiar, personal paramédico) deben integrar al expediente.",
                "Informe Semanal (previo-definitivo).",
                "Informes mensuales de productividad.",
            ],
        },
    },
    "V. Indicadores Médicos": {
        "icono": "📈",
        "descripcion": "Indicadores de atención médica, coberturas y productividad en servicios de salud.",
        "subtemas": {
            "Informes Mensuales de Coberturas": [
                "Programa Salud del Niño: Nutrición, Prevención y Control, Detección de Enfermedades.",
                "Programa Salud del Adolescente: Nutrición, Prevención, Salud Reproductiva.",
                "Programa Salud de la Mujer: Nutrición, Prevención, Salud Reproductiva.",
                "Programa Salud del Hombre: Nutrición, Prevención, Salud Reproductiva.",
                "Programa Salud del Adulto Mayor: Nutrición, Prevención, Detección.",
            ],
            "Indicadores de Atención Médica": [
                "% de derechohabientes atendidos por cita previa, horario concertado y espontáneos.",
                "% de derechohabientes según tiempo de espera para consulta de medicina familiar.",
                "% de derechohabientes referidos a segundo nivel.",
                "% de derechohabientes en control adecuado de hipertensión arterial.",
                "% de derechohabientes en control adecuado de diabetes mellitus tipo II.",
                "% de embarazadas con auscultación de frecuencia cardiaca fetal.",
                "% que esperan menos de 30 minutos para consulta (cita previa, horario concertado, espontáneos).",
            ],
            "Atención Preventiva Integrada": [
                "Atención preventiva según derechohabiencia, lugar, servicio y grupo programático.",
                "Atención preventiva integrada en derechohabientes por enfermera.",
            ],
            "Planificación Familiar": [
                "Aceptantes por Tipo de Método Anticonceptivo y Grupo de Edad.",
                "Consultas Subsecuentes por Médico Familiar según método.",
                "Consultas Subsecuentes por Enfermería según método.",
                "Consumo mensual de productos anticonceptivos.",
            ],
            "Salud en el Trabajo": [
                "Días de incapacidad por pacientes (total, enfermedad general, riesgo de trabajo).",
                "Total de motivos de atención que generaron días de incapacidad (por lista mexicana).",
            ],
            "Salud Materna": [
                "Embarazo, puerperio y sus complicaciones.",
                "Climaterio y menopausia.",
                "Vigilancia materna.",
            ],
        },
    },
    "VI. Clasificación Internacional de Enfermedades (CIE-10)": {
        "icono": "🏷️",
        "descripcion": "Principios de codificación con la CIE-10 para morbilidad y mortalidad.",
        "subtemas": {
            "Estructura de la CIE-10": [
                "22 capítulos organizados por aparatos y sistemas.",
                "Códigos alfanuméricos de 3 a 4 caracteres (letra + números).",
                "Cap. I (A00-B99): Enfermedades infecciosas y parasitarias.",
                "Cap. II (C00-D48): Neoplasias.",
                "Cap. IV (E00-E90): Enfermedades endocrinas, de la nutrición y metabólicas.",
                "Cap. IX (I00-I99): Enfermedades del sistema circulatorio.",
                "Cap. X (J00-J99): Enfermedades del sistema respiratorio.",
                "Cap. XV (O00-O99): Embarazo, parto y puerperio.",
                "Cap. XVI (P00-P96): Ciertas afecciones originadas en el periodo perinatal.",
                "Cap. XVII (Q00-Q99): Malformaciones congénitas.",
                "Cap. XX (V01-Y98): Causas externas de morbilidad y mortalidad.",
            ],
            "Codificación de Morbilidad": [
                "La codificación debe efectuarse al nivel de 4 dígitos según la NOM-035.",
                "Se utiliza para registrar motivos de consulta y diagnósticos.",
                "Lista mexicana de enfermedades.",
            ],
            "Codificación de Mortalidad - Pasos de Selección": [
                "SP1: Causa única en el Certificado.",
                "SP2: Solo una línea utilizada en la Parte 1.",
                "SP3: Más de una línea usada en la Parte 1.",
                "SP4: Hay Secuencia (antes R1).",
                "SP5: No Hay Secuencia (antes R2).",
                "SP6: Causa Obvia (antes R3).",
                "SP7: Afecciones 'Mal Definidas' (antes RA).",
                "SP8: Afecciones 'Poco Probables de Causar la Muerte' (antes RB).",
            ],
            "Codificación de Mortalidad - Pasos de Modificación": [
                "M1: Asociación (antes RC).",
                "M2: Especificidad (antes RD).",
                "M3: Volver a comprobar pasos SP6, M1 y M2.",
                "M4: Instrucciones sobre procedimientos médicos, envenenamiento, lesiones principales, muertes maternas.",
            ],
        },
    },
    "VII. Mortalidad y Certificado de Defunción": {
        "icono": "📋",
        "descripcion": "Certificado de defunción, causa básica de muerte, secuencias aceptadas y rechazadas.",
        "subtemas": {
            "Certificado de Defunción": [
                "El certificado de defunción tiene Parte 1 y Parte 2.",
                "Parte 1: Secuencia causal (a, b, c, d) de la causa directa a la causa básica.",
                "Parte 2: Otros estados patológicos significativos que contribuyeron a la muerte.",
                "La causa básica de defunción es el objetivo principal de la codificación.",
            ],
            "Secuencias Aceptadas": [
                "Enfermedades infecciosas debidas a otras afecciones (con excepciones).",
                "VIH/SIDA debido a: afecciones que requieren transfusiones, procedimientos invasivos, abuso de drogas.",
                "Diabetes mellitus tipo 1 (E10) debida a destrucción autoinmune de células β.",
                "Diabetes mellitus tipo 2 (E11) debida a resistencia a la insulina.",
                "Fiebre reumática (I00-I02) debida a fiebre escarlatina (A38).",
                "Caídas (W00-W19) debidas a trastorno de la densidad ósea (M80-M85).",
                "Asfixia y aspiración (W78-W80) debidas a otras causas.",
                "Enfermedades circulatorias agudas debidas a tumores malignos, diabetes o asma.",
            ],
            "Secuencias Rechazadas": [
                "No se acepta tumor maligno como debido a cualquier otra enfermedad (excepto ciertos tumores debidos a VIH).",
                "No se acepta hemofilia (D66, D67) como debida a cualquier otra enfermedad.",
                "No se acepta influenza (J09-J11) como debida a cualquier otra causa.",
                "No se acepta anomalía congénita (Q00-Q99) como debida a cualquier causa (excepciones: anomalía cromosómica, hipoplasia pulmonar).",
                "No se acepta suicidio (X60-X84) como debido a otras afecciones.",
                "No se acepta aterosclerosis como consecuencia de un tumor.",
                "No se acepta cardiopatía isquémica crónica (I20, I25) como debida a un tumor.",
            ],
            "Mortalidad Materna": [
                "O95.X: Muerte obstétrica de causa no especificada (durante embarazo, parto o puerperio).",
                "O96.X: Muerte materna por causa obstétrica que ocurre después de 42 días pero antes de un año.",
                "O97.X: Muerte por secuela de causa obstétrica directa, un año o más después de la terminación del embarazo.",
                "Si la fallecida es mujer y hay embarazo/parto/puerperio reportado, determinar si se codifica en Capítulo XV.",
            ],
            "Presunción de Causa Intercurrente": [
                "Se autoriza la presunción de causa intercurrente para aceptar una secuencia como fue informada.",
                "No se debe utilizar para cambiar la codificación.",
                "Ejemplo: hematemesis debida a cirrosis (secuencia real: cirrosis→hipertensión portal→várices esofágicas rotas→hematemesis).",
            ],
        },
    },
    "VIII. Procesos Operativos del ARIMAC": {
        "icono": "⚙️",
        "descripcion": "Procesos de captura, validación, envío de información y cierre de periodos.",
        "subtemas": {
            "Proceso de Integración al DataMart": [
                "El ARIMAC codifica y captura la información.",
                "En UMF: registran diario el formato RAIS y transfieren consultas SIMF→SIAIS.",
                "En hospitales 2do y 3er nivel: capturan formatos 4-30-6 y 4-30-6P/90.",
                "Al cierre de mes: SIAIS-SIMO generan archivos TXT de subsistemas 10, 13, 27, 31 y 32.",
                "El proceso de validación se repite hasta eliminar inconsistencias.",
            ],
            "Cierre de Información": [
                "La UMAE o Delegación monitorea el envío de información de las unidades.",
                "Confirmada la transferencia, se ejecuta el cierre delegacional.",
                "La DIS monitorea que el 100% de delegaciones y UMAEs concluyan el cierre mensual.",
                "Se realiza el cierre nacional.",
            ],
            "Subsistemas del DataMart": [
                "Formatos Manuales: 12 (Trasplantes), 14 (Censo Población), 15 (Consumo Víveres), 19 (Subrogados), 29 (Preventivas Hospital), 43-49 (Formación y Educación).",
                "Automatizados: 10 (Población y Servicios), 13 (Egresos Hospitalarios), 27 (Motivos de Demanda), 31 (Actividades), 32.",
                "La DIS actualiza catálogos antes de cada cierre nacional.",
            ],
            "Análisis de la Información": [
                "El Director y Jefatura de departamento clínico de la unidad son responsables del análisis.",
                "Los cuadros electrónicos no deben imprimirse todos, solo los requeridos por la dirección.",
                "Las delegaciones pueden generar reportes predefinidos o consultas no planeadas del DataMart.",
            ],
        },
    },
}


# ============================================================
# BANCO DE PREGUNTAS
# ============================================================

PREGUNTAS = [
    # --- NORMATIVIDAD ---
    {
        "tema": "I. Normatividad y Marco Legal",
        "pregunta": "¿Cuál es el objetivo de la NOM-035-SSA3-2012?",
        "opciones": [
            "Regular la prestación de servicios de urgencias médicas",
            "Establecer criterios y procedimientos para producir, captar, integrar, procesar, sistematizar, evaluar y divulgar la Información en Salud",
            "Normar el uso de medicamentos controlados",
            "Establecer los lineamientos para la construcción de hospitales",
        ],
        "respuesta": 1,
        "explicacion": "La NOM-035-SSA3-2012 tiene por objeto establecer los criterios y procedimientos para producir, captar, integrar, procesar, sistematizar, evaluar y divulgar la Información en Salud.",
    },
    {
        "tema": "I. Normatividad y Marco Legal",
        "pregunta": "¿Qué significan las siglas CLUES?",
        "opciones": [
            "Clasificación Única de Establecimientos Sanitarios",
            "Clave Única de Establecimientos de Salud",
            "Centro Logístico Unificado de Establecimientos de Salud",
            "Catálogo Universal de Entidades de Salud",
        ],
        "respuesta": 1,
        "explicacion": "CLUES significa Clave Única de Establecimientos de Salud. Todo establecimiento del SNS debe contar con CLUES.",
    },
    {
        "tema": "I. Normatividad y Marco Legal",
        "pregunta": "¿Cuáles son los atributos de calidad que debe cumplir la información según la NOM-035?",
        "opciones": [
            "Rapidez, Exactitud, Presentación, Formato",
            "Oportunidad, Cobertura, Integridad, Confiabilidad, Validez y Consistencia",
            "Claridad, Brevedad, Utilidad, Economía",
            "Disponibilidad, Accesibilidad, Legibilidad, Portabilidad",
        ],
        "respuesta": 1,
        "explicacion": "Los atributos de calidad según la NOM-035 son: Oportunidad, Cobertura, Integridad, Confiabilidad, Validez y Consistencia.",
    },
    {
        "tema": "I. Normatividad y Marco Legal",
        "pregunta": "¿A cuántos dígitos debe efectuarse la codificación con clasificaciones internacionales (CIE, CIF, CIE-MC) según la NOM-035?",
        "opciones": [
            "3 dígitos",
            "4 dígitos",
            "5 dígitos",
            "2 dígitos",
        ],
        "respuesta": 1,
        "explicacion": "Según la NOM-035, en todos los casos en que sea necesario utilizar las clasificaciones internacionales, la codificación debe efectuarse al nivel de cuatro dígitos.",
    },
    {
        "tema": "I. Normatividad y Marco Legal",
        "pregunta": "¿Qué significan las siglas SINAIS?",
        "opciones": [
            "Sistema Nacional de Indicadores en Salud",
            "Subsistema Nacional de Información y Análisis en Salud",
            "Sistema Nacional de Información en Salud",
            "Servicio Nacional de Informática en Salud",
        ],
        "respuesta": 2,
        "explicacion": "SINAIS significa Sistema Nacional de Información en Salud.",
    },
    {
        "tema": "I. Normatividad y Marco Legal",
        "pregunta": "¿En qué fecha fue publicada la Ley Federal de Archivos en el DOF?",
        "opciones": [
            "15 de marzo de 2010",
            "23 de enero de 2012",
            "04 de mayo de 2015",
            "26 de enero de 2017",
        ],
        "respuesta": 1,
        "explicacion": "La Ley Federal de Archivos fue publicada en el Diario Oficial de la Federación el 23 de enero de 2012.",
    },
    {
        "tema": "I. Normatividad y Marco Legal",
        "pregunta": "Según la Ley Federal de Archivos, ¿qué es un 'Archivo de concentración'?",
        "opciones": [
            "Unidad responsable de documentos de uso cotidiano",
            "Unidad responsable de la administración de documentos cuya consulta es esporádica",
            "Lugar donde se guardan los expedientes clínicos activos",
            "Base de datos digital de documentos escaneados",
        ],
        "respuesta": 1,
        "explicacion": "Archivo de concentración: unidad responsable de la administración de documentos cuya consulta es esporádica por parte de las unidades administrativas.",
    },
    {
        "tema": "I. Normatividad y Marco Legal",
        "pregunta": "¿Qué significan las siglas MAAGTIC?",
        "opciones": [
            "Manual Administrativo de Aplicación General para las Tecnologías de la Información y la Comunicación",
            "Manual de Actividades Administrativas Generales en TIC",
            "Método de Análisis y Aplicación General de Tecnología e Información Clínica",
            "Marco de Arquitectura y Administración General de TIC",
        ],
        "respuesta": 0,
        "explicacion": "MAAGTIC = Manual Administrativo de Aplicación General para las Tecnologías de la Información y la Comunicación.",
    },
    {
        "tema": "I. Normatividad y Marco Legal",
        "pregunta": "¿Qué significan las siglas DGIS?",
        "opciones": [
            "Departamento General de Información del SNS",
            "Dirección General de Información en Salud",
            "División General de Indicadores en Salud",
            "Dirección de Gestión de Información del Sector Salud",
        ],
        "respuesta": 1,
        "explicacion": "DGIS = Dirección General de Información en Salud.",
    },
    {
        "tema": "I. Normatividad y Marco Legal",
        "pregunta": "¿Qué significan las siglas SEED?",
        "opciones": [
            "Sistema Estadístico de Enfermedades y Diagnósticos",
            "Subsistema Epidemiológico y Estadístico de Defunciones",
            "Servicio Estatal de Estadísticas de Defunciones",
            "Sistema Electrónico de Estadísticas y Datos",
        ],
        "respuesta": 1,
        "explicacion": "SEED = Subsistema Epidemiológico y Estadístico de Defunciones.",
    },
    # --- EXPEDIENTE CLÍNICO ---
    {
        "tema": "II. Expediente Clínico y ARIMAC",
        "pregunta": "¿Qué significan las siglas ARIMAC?",
        "opciones": [
            "Área de Registros e Información Médica y Archivos Centrales",
            "Área de Información Médica y Archivo Clínico",
            "Archivo de Registro e Información de Medicina y Atención Clínica",
            "Administración de Registros de Información Médica y Archivo Clínico",
        ],
        "respuesta": 1,
        "explicacion": "ARIMAC = Área de Información Médica y Archivo Clínico.",
    },
    {
        "tema": "II. Expediente Clínico y ARIMAC",
        "pregunta": "¿Cuánto tiempo mínimo deben conservarse los expedientes clínicos?",
        "opciones": [
            "3 años",
            "5 años",
            "10 años",
            "15 años",
        ],
        "respuesta": 1,
        "explicacion": "Los expedientes clínicos deben conservarse por un mínimo de 5 años.",
    },
    {
        "tema": "II. Expediente Clínico y ARIMAC",
        "pregunta": "¿De qué manera deben ir acomodados los documentos dentro del expediente clínico?",
        "opciones": [
            "Alfabéticamente",
            "Por tipo de documento",
            "De manera cronológica",
            "Por importancia clínica",
        ],
        "respuesta": 2,
        "explicacion": "Los documentos del expediente clínico deben ir acomodados de manera cronológica.",
    },
    {
        "tema": "II. Expediente Clínico y ARIMAC",
        "pregunta": "¿Cuáles son las etapas del procedimiento del Archivo Clínico?",
        "opciones": [
            "Recepción, Clasificación, Almacenamiento, Destrucción",
            "Apertura, Integración, Control, Revisión sistemática, Depuración",
            "Ingreso, Registro, Consulta, Egreso",
            "Creación, Modificación, Consulta, Eliminación",
        ],
        "respuesta": 1,
        "explicacion": "Las etapas del procedimiento son: Apertura, Integración, Control, Revisión sistemática de la vigencia y valor documental, y Depuración.",
    },
    {
        "tema": "II. Expediente Clínico y ARIMAC",
        "pregunta": "¿Qué tipo de documento es el expediente clínico?",
        "opciones": [
            "Un documento exclusivamente administrativo",
            "Un documento médico-legal y base para la asistencia, docencia e investigación",
            "Un documento meramente estadístico",
            "Un documento de uso interno sin valor legal",
        ],
        "respuesta": 1,
        "explicacion": "El expediente clínico es un documento médico-legal y es la base para la asistencia, docencia e investigación en medicina.",
    },
    # --- SISTEMAS DE INFORMACIÓN ---
    {
        "tema": "III. Sistemas de Información en Salud",
        "pregunta": "¿En qué año se desarrolló el DataMart Estadísticas Médicas?",
        "opciones": [
            "2001",
            "2003",
            "2005",
            "2007",
        ],
        "respuesta": 1,
        "explicacion": "El DataMart Estadísticas Médicas fue desarrollado en 2003 por la División de Información en Salud en coordinación con la División de Sistemas de Soporte.",
    },
    {
        "tema": "III. Sistemas de Información en Salud",
        "pregunta": "¿En cuántas delegaciones (CIAE) opera actualmente el DataMart?",
        "opciones": [
            "25",
            "30",
            "35",
            "40",
        ],
        "respuesta": 2,
        "explicacion": "El DataMart opera en 35 delegaciones (CIAE) y 25 UMAE.",
    },
    {
        "tema": "III. Sistemas de Información en Salud",
        "pregunta": "¿Qué es el DataMart EM?",
        "opciones": [
            "Un programa de correo electrónico del IMSS",
            "Un conjunto de componentes de hardware y software que almacenan grandes volúmenes de datos (repositorio) para el análisis y toma de decisiones",
            "Un formato manual de captura de información",
            "Un módulo del expediente clínico electrónico",
        ],
        "respuesta": 1,
        "explicacion": "DataMart EM es un conjunto de componentes de hardware y software que almacenan grandes volúmenes de datos (Repositorio) para analizar de manera prospectiva, apuntando hacia un sistema de información gerencial para toma de decisiones.",
    },
    {
        "tema": "III. Sistemas de Información en Salud",
        "pregunta": "¿Qué es un Data Warehouse en el contexto del IMSS?",
        "opciones": [
            "Un almacén físico de documentos",
            "Un servidor de respaldo",
            "Un conjunto de DataMarts que mantienen las mismas características",
            "Una base de datos de recursos humanos",
        ],
        "respuesta": 2,
        "explicacion": "Data Warehouse es un conjunto de DataMarts EM que mantienen las mismas características de un DataMart.",
    },
    {
        "tema": "III. Sistemas de Información en Salud",
        "pregunta": "¿Cuáles son los módulos del SIMO Central?",
        "opciones": [
            "Urgencias, Hospitalización y Quirófano",
            "Consulta Externa, Hospitalización y Enlace",
            "Admisión, Tratamiento y Egreso",
            "Laboratorio, Imagenología y Farmacia",
        ],
        "respuesta": 1,
        "explicacion": "Los módulos del SIMO Central son: Consulta Externa, Hospitalización y Enlace.",
    },
    {
        "tema": "III. Sistemas de Información en Salud",
        "pregunta": "¿Qué formato se registra diariamente en las unidades de medicina familiar?",
        "opciones": [
            "Formato 4-30-6",
            "Formato RAIS",
            "Formato SUIVE",
            "Formato DataMart",
        ],
        "respuesta": 1,
        "explicacion": "En las unidades de medicina familiar se registra diariamente el formato RAIS (Registro de Actividades de Atención Integral de la Salud).",
    },
    {
        "tema": "III. Sistemas de Información en Salud",
        "pregunta": "¿Qué subsistemas automatizados genera el SIAIS/SIMO Central?",
        "opciones": [
            "12, 14, 15, 19, 29",
            "10, 13, 27, 31, 32",
            "43, 46, 47, 48, 49",
            "1, 2, 3, 4, 5",
        ],
        "respuesta": 1,
        "explicacion": "Los subsistemas automatizados (SIAIS/SIMO Central) son: 10 (Población y Servicios), 13 (Egresos Hospitalarios), 27 (Motivos de Demanda), 31 (Actividades) y 32.",
    },
    {
        "tema": "III. Sistemas de Información en Salud",
        "pregunta": "¿En qué tecnología está desarrollado el DataMart?",
        "opciones": [
            "Tecnología cliente-servidor",
            "Tecnología WEB",
            "Tecnología de escritorio",
            "Tecnología mainframe",
        ],
        "respuesta": 1,
        "explicacion": "El DataMart Estadísticas Médicas está desarrollado en tecnología WEB.",
    },
    {
        "tema": "III. Sistemas de Información en Salud",
        "pregunta": "¿Qué significan las siglas SIMF?",
        "opciones": [
            "Sistema de Información de Morbilidad Frecuente",
            "Sistema de Información de Medicina Familiar",
            "Sistema Integral de Monitoreo Funcional",
            "Subsistema de Informática Médica Federal",
        ],
        "respuesta": 1,
        "explicacion": "SIMF = Sistema de Información de Medicina Familiar.",
    },
    # --- VIGILANCIA EPIDEMIOLÓGICA ---
    {
        "tema": "IV. Vigilancia Epidemiológica",
        "pregunta": "¿Qué nomenclatura tiene el archivo de enlace SUAVE del informe semanal?",
        "opciones": [
            "INFEE00SS.TXT",
            "BAEE00SS.DBF",
            "SEMEE00SS.XLS",
            "SUAVEE00SS.CSV",
        ],
        "respuesta": 1,
        "explicacion": "El archivo de enlace SUAVE se genera con la nomenclatura BAEE00SS.DBF, donde EE = clave del Estado y SS = número de la semana.",
    },
    {
        "tema": "IV. Vigilancia Epidemiológica",
        "pregunta": "¿A qué plataforma se sube el archivo del Informe Semanal?",
        "opciones": [
            "DataMart EM",
            "IBSv2 Informe Semanal",
            "SIMO Central",
            "SEED Online",
        ],
        "respuesta": 1,
        "explicacion": "Se sube el archivo de enlace a la plataforma IBSv2 Informe Semanal y se informa al Epidemiólogo para su validación.",
    },
    {
        "tema": "IV. Vigilancia Epidemiológica",
        "pregunta": "¿Quién es responsable de integrar la información de todas las unidades del informe semanal y subirla a la plataforma IBSv2?",
        "opciones": [
            "El Director de la Unidad",
            "El Médico Familiar",
            "La CIAE",
            "El ARIMAC de cada unidad",
        ],
        "respuesta": 2,
        "explicacion": "La CIAE (Coordinación de Información y Análisis Estratégico) es responsable de integrar la información de todas las unidades y subirla a la plataforma IBSv2.",
    },
    {
        "tema": "IV. Vigilancia Epidemiológica",
        "pregunta": "¿Qué significan las siglas RAIS?",
        "opciones": [
            "Registro Administrativo de Información en Salud",
            "Registro de Actividades de Atención Integral de la Salud",
            "Reporte Analítico de Indicadores de Salud",
            "Resumen de Atención Integral y Seguimiento",
        ],
        "respuesta": 1,
        "explicacion": "RAIS = Registro de Actividades de Atención Integral de la Salud, en Medicina Familiar.",
    },
    # --- INDICADORES ---
    {
        "tema": "V. Indicadores Médicos",
        "pregunta": "¿Cuánto tiempo de espera es considerado como indicador de calidad para la consulta de medicina familiar?",
        "opciones": [
            "Menos de 15 minutos",
            "Menos de 30 minutos",
            "Menos de 45 minutos",
            "Menos de 60 minutos",
        ],
        "respuesta": 1,
        "explicacion": "El indicador mide el porcentaje de derechohabientes que esperan menos de 30 minutos para recibir consulta en medicina familiar.",
    },
    {
        "tema": "V. Indicadores Médicos",
        "pregunta": "¿Cuáles son las modalidades de atención en medicina familiar según los indicadores?",
        "opciones": [
            "Consulta general, especializada y de urgencia",
            "Cita previa, horario concertado y espontáneo sin cita",
            "Primera vez, subsecuente y referencia",
            "Matutina, vespertina y nocturna",
        ],
        "respuesta": 1,
        "explicacion": "Las modalidades son: cita previa, horario concertado y espontáneo sin cita.",
    },
    {
        "tema": "V. Indicadores Médicos",
        "pregunta": "¿Qué dos enfermedades crónicas tienen indicadores de control adecuado en medicina familiar?",
        "opciones": [
            "Cáncer y EPOC",
            "Hipertensión arterial y diabetes mellitus tipo II",
            "Artritis y osteoporosis",
            "Asma e insuficiencia renal",
        ],
        "respuesta": 1,
        "explicacion": "Los indicadores miden el % de derechohabientes en control adecuado de hipertensión arterial y diabetes mellitus tipo II.",
    },
    # --- CIE-10 ---
    {
        "tema": "VI. Clasificación Internacional de Enfermedades (CIE-10)",
        "pregunta": "¿Cuántos capítulos tiene la CIE-10?",
        "opciones": [
            "18",
            "20",
            "22",
            "25",
        ],
        "respuesta": 2,
        "explicacion": "La CIE-10 tiene 22 capítulos organizados por aparatos y sistemas.",
    },
    {
        "tema": "VI. Clasificación Internacional de Enfermedades (CIE-10)",
        "pregunta": "¿Qué paso de selección de mortalidad se aplica cuando hay una sola causa en el certificado?",
        "opciones": [
            "SP2",
            "SP1",
            "SP3",
            "M1",
        ],
        "respuesta": 1,
        "explicacion": "SP1: Se aplica cuando hay una causa única en el Certificado de defunción.",
    },
    {
        "tema": "VI. Clasificación Internacional de Enfermedades (CIE-10)",
        "pregunta": "¿A qué corresponde el paso M1 en la codificación de mortalidad?",
        "opciones": [
            "Especificidad",
            "Causa Obvia",
            "Asociación",
            "Afecciones Mal Definidas",
        ],
        "respuesta": 2,
        "explicacion": "M1 corresponde a Asociación (antes conocida como RC).",
    },
    {
        "tema": "VI. Clasificación Internacional de Enfermedades (CIE-10)",
        "pregunta": "¿Qué paso de selección se aplica cuando hay más de una línea utilizada en la Parte 1 del certificado?",
        "opciones": [
            "SP1",
            "SP2",
            "SP3",
            "SP4",
        ],
        "respuesta": 2,
        "explicacion": "SP3: Se aplica cuando hay más de una línea usada en la Parte 1 del certificado.",
    },
    {
        "tema": "VI. Clasificación Internacional de Enfermedades (CIE-10)",
        "pregunta": "¿Cuál es el rango de códigos CIE-10 para Enfermedades infecciosas y parasitarias?",
        "opciones": [
            "C00-D48",
            "A00-B99",
            "I00-I99",
            "J00-J99",
        ],
        "respuesta": 1,
        "explicacion": "Capítulo I: Enfermedades infecciosas y parasitarias corresponde a los códigos A00-B99.",
    },
    {
        "tema": "VI. Clasificación Internacional de Enfermedades (CIE-10)",
        "pregunta": "¿A qué corresponde el paso SP7 en la codificación de mortalidad?",
        "opciones": [
            "Causa Obvia",
            "No Hay Secuencia",
            "Afecciones 'Mal Definidas'",
            "Especificidad",
        ],
        "respuesta": 2,
        "explicacion": "SP7 corresponde a Afecciones 'Mal Definidas' (antes conocida como Regla A).",
    },
    {
        "tema": "VI. Clasificación Internacional de Enfermedades (CIE-10)",
        "pregunta": "¿Qué paso de modificación se ocupa de las instrucciones sobre procedimientos médicos, envenenamiento, lesiones principales y muertes maternas?",
        "opciones": [
            "M1",
            "M2",
            "M3",
            "M4",
        ],
        "respuesta": 3,
        "explicacion": "M4: Instrucciones sobre procedimientos médicos, envenenamiento, lesiones principales y muertes maternas.",
    },
    # --- MORTALIDAD ---
    {
        "tema": "VII. Mortalidad y Certificado de Defunción",
        "pregunta": "¿Se acepta el tumor maligno como consecuencia de cualquier otra enfermedad?",
        "opciones": [
            "Sí, siempre",
            "No, excepto ciertos tumores debidos al VIH",
            "Sí, solo en menores de edad",
            "No, sin ninguna excepción",
        ],
        "respuesta": 1,
        "explicacion": "No se acepta un tumor maligno como debido a cualquier otra enfermedad, excepto ciertos tumores malignos como debidos al VIH (ej. Sarcoma de Kaposi C46, Linfoma de Burkitt C83.7).",
    },
    {
        "tema": "VII. Mortalidad y Certificado de Defunción",
        "pregunta": "¿Se acepta la influenza (J09-J11) como debida a cualquier otra causa?",
        "opciones": [
            "Sí, si es debida a VIH",
            "Sí, si es debida a diabetes",
            "No, no se acepta como debida a cualquier otra causa",
            "Sí, si es debida a enfermedades respiratorias crónicas",
        ],
        "respuesta": 2,
        "explicacion": "No se acepta la influenza (gripe) (J09-J11) como debida a cualquier otra causa. Es una secuencia rechazada.",
    },
    {
        "tema": "VII. Mortalidad y Certificado de Defunción",
        "pregunta": "¿Qué código se utiliza para la muerte obstétrica de causa no especificada?",
        "opciones": [
            "O96.X",
            "O97.X",
            "O95.X",
            "O99.X",
        ],
        "respuesta": 2,
        "explicacion": "O95.X: Muerte obstétrica de causa no especificada. Se usa cuando la mujer muere durante el embarazo, parto o puerperio y la única información es 'muerte materna' u 'obstétrica'.",
    },
    {
        "tema": "VII. Mortalidad y Certificado de Defunción",
        "pregunta": "¿Se aceptan las caídas (W00-W19) como debidas a un trastorno de la densidad ósea (M80-M85)?",
        "opciones": [
            "No, nunca se aceptan accidentes como debidos a enfermedades",
            "Sí, es una secuencia aceptada",
            "Solo en adultos mayores",
            "Solo si la caída ocurrió en el hospital",
        ],
        "respuesta": 1,
        "explicacion": "Sí, se aceptan las caídas (W00-W19) como debidas a un trastorno de la densidad ósea (M80-M85). Es una de las excepciones en secuencias aceptadas para accidentes.",
    },
    {
        "tema": "VII. Mortalidad y Certificado de Defunción",
        "pregunta": "¿Qué código se usa para la muerte materna por causa obstétrica después de 42 días pero antes de un año?",
        "opciones": [
            "O95.X",
            "O96.X",
            "O97.X",
            "O98.X",
        ],
        "respuesta": 1,
        "explicacion": "O96.X: Muerte materna por una causa obstétrica que ocurre después de 42 días, pero antes de un año tras la terminación del embarazo.",
    },
    # --- PROCESOS OPERATIVOS ---
    {
        "tema": "VIII. Procesos Operativos del ARIMAC",
        "pregunta": "¿Qué formatos se capturan en unidades hospitalarias de 2do y 3er nivel?",
        "opciones": [
            "Formato RAIS",
            "Formatos 4-30-6 y 4-30-6P/90",
            "Formato SUIVE",
            "Formato DataMart",
        ],
        "respuesta": 1,
        "explicacion": "En unidades hospitalarias de 2do y 3er nivel se capturan los formatos de consulta externa de especialidades 4-30-6 y 4-30-6P/90.",
    },
    {
        "tema": "VIII. Procesos Operativos del ARIMAC",
        "pregunta": "¿Quién monitorea que el 100% de las delegaciones y UMAEs concluyan el cierre mensual?",
        "opciones": [
            "La CIAE",
            "El ARIMAC de cada unidad",
            "La DIS (División de Información en Salud)",
            "La DIDT",
        ],
        "respuesta": 2,
        "explicacion": "La DIS (División de Información en Salud) monitorea que el 100% de las delegaciones y UMAEs concluyan el cierre del mes correspondiente, y realiza el cierre nacional.",
    },
    {
        "tema": "VIII. Procesos Operativos del ARIMAC",
        "pregunta": "¿Qué tipo de archivos generan los sistemas SIAIS-SIMO al cierre de mes?",
        "opciones": [
            "Archivos PDF",
            "Archivos Excel (XLS)",
            "Archivos tipo texto (TXT)",
            "Archivos de base de datos (MDB)",
        ],
        "respuesta": 2,
        "explicacion": "Al cierre de mes, los sistemas SIAIS-SIMO Central generan archivos tipo texto (TXT) de los subsistemas: 10, 13, 27, 31 y 32.",
    },
    {
        "tema": "VIII. Procesos Operativos del ARIMAC",
        "pregunta": "¿Qué significan las siglas CIAE?",
        "opciones": [
            "Centro de Investigación y Análisis Estadístico",
            "Coordinación de Información y Análisis Estratégico",
            "Comité de Información y Administración Estadística",
            "Central de Integración y Análisis Epidemiológico",
        ],
        "respuesta": 1,
        "explicacion": "CIAE = Coordinación de Información y Análisis Estratégico.",
    },
    {
        "tema": "VIII. Procesos Operativos del ARIMAC",
        "pregunta": "¿Qué significan las siglas OIMAC?",
        "opciones": [
            "Oficina de Indicadores Médicos y Archivo Central",
            "Oficina de Información Médica y Archivo Clínico",
            "Organización Integral de Manejo de Archivos Clínicos",
            "Operación de Información y Manejo de Archivos Clínicos",
        ],
        "respuesta": 1,
        "explicacion": "OIMAC = Oficina de Información Médica y Archivo Clínico (en las UMAE).",
    },
    {
        "tema": "VIII. Procesos Operativos del ARIMAC",
        "pregunta": "¿Qué subsistema corresponde a 'Informe Complementario Trasplantes y Donación de Órganos'?",
        "opciones": [
            "Subsistema 10",
            "Subsistema 12",
            "Subsistema 14",
            "Subsistema 19",
        ],
        "respuesta": 1,
        "explicacion": "El subsistema 12 corresponde al Informe Complementario Trasplantes y Donación de Órganos (formato manual, captura mensual).",
    },
    {
        "tema": "VIII. Procesos Operativos del ARIMAC",
        "pregunta": "¿Qué subsistema corresponde al 'Censo de Población Adscrita a Médico Familiar'?",
        "opciones": [
            "Subsistema 10",
            "Subsistema 12",
            "Subsistema 14",
            "Subsistema 15",
        ],
        "respuesta": 2,
        "explicacion": "El subsistema 14 corresponde al Censo de Población Adscrita a Médico Familiar (formato manual, captura anual).",
    },
    # --- NORMATIVIDAD (adicionales) ---
    {
        "tema": "I. Normatividad y Marco Legal",
        "pregunta": "Según el Artículo 107 de la Ley General de Salud, ¿qué deben llevar los establecimientos de salud?",
        "opciones": [
            "Un registro de asistencia del personal",
            "Un padrón de proveedores autorizados",
            "Sistemas de información",
            "Un inventario de medicamentos",
        ],
        "respuesta": 2,
        "explicacion": "El Art. 107 de la Ley General de Salud establece que los establecimientos que presten servicios de salud llevarán sistemas de información.",
    },
    {
        "tema": "I. Normatividad y Marco Legal",
        "pregunta": "¿En qué fecha fue publicada la Ley General de Transparencia y Acceso a la Información Pública en el DOF?",
        "opciones": [
            "04 de mayo de 2015",
            "23 de enero de 2012",
            "26 de enero de 2017",
            "15 de septiembre de 2014",
        ],
        "respuesta": 0,
        "explicacion": "La Ley General de Transparencia y Acceso a la Información Pública fue publicada en el DOF el 04 de mayo de 2015. Es el primer ordenamiento que regula el tratamiento de datos personales en el sector público.",
    },
    {
        "tema": "I. Normatividad y Marco Legal",
        "pregunta": "Según la Ley Federal de Archivos, ¿qué es el 'Archivo de trámite'?",
        "opciones": [
            "Unidad de documentos de consulta esporádica",
            "Documentos de conservación permanente",
            "Base de datos de documentos digitalizados",
            "Unidad responsable de los documentos de uso cotidiano",
        ],
        "respuesta": 3,
        "explicacion": "El Archivo de trámite es la unidad responsable de la administración de documentos de uso cotidiano y necesario para el ejercicio de las atribuciones de una unidad administrativa.",
    },
    # --- EXPEDIENTE CLÍNICO (adicionales) ---
    {
        "tema": "II. Expediente Clínico y ARIMAC",
        "pregunta": "¿Cómo se define el expediente clínico?",
        "opciones": [
            "Conjunto único de información y datos personales de un paciente",
            "Listado de recetas médicas emitidas",
            "Registro contable de servicios otorgados",
            "Carpeta con documentos administrativos de la unidad",
        ],
        "respuesta": 0,
        "explicacion": "El expediente clínico es el conjunto único de información y datos personales de un paciente, integrado por documentos escritos, gráficos, imagenológicos, electrónicos, magnéticos, etc.",
    },
    {
        "tema": "II. Expediente Clínico y ARIMAC",
        "pregunta": "¿Cuáles son los tipos de documentos que se manejan en el Archivo Clínico?",
        "opciones": [
            "Originales, copias y duplicados",
            "Documentos activos, pasivos y cancelados",
            "Documentos de archivo, de comprobación administrativa inmediata y de apoyo informativo",
            "Documentos médicos, de enfermería y administrativos",
        ],
        "respuesta": 2,
        "explicacion": "Los tipos de documentos son: Documentos de archivo, Documentos de comprobación administrativa inmediata y Documentos de apoyo informativo.",
    },
    {
        "tema": "II. Expediente Clínico y ARIMAC",
        "pregunta": "¿Dónde deben estar contenidos los documentos del expediente clínico?",
        "opciones": [
            "En un sobre sellado",
            "Dentro de una carpeta de contención debidamente identificada",
            "En cajas de archivo muerto",
            "En el área de trabajo social",
        ],
        "respuesta": 1,
        "explicacion": "El expediente clínico debe estar dentro de una carpeta de contención debidamente identificada.",
    },
    {
        "tema": "II. Expediente Clínico y ARIMAC",
        "pregunta": "¿Cómo se deben guardar los cuadros electrónicos generados?",
        "opciones": [
            "En una sola carpeta general",
            "En el escritorio de la computadora",
            "En discos compactos por semana",
            "En carpetas anuales y subcarpetas por mes",
        ],
        "respuesta": 3,
        "explicacion": "Los cuadros electrónicos se deben guardar en carpetas anuales y subcarpetas por mes.",
    },
    {
        "tema": "II. Expediente Clínico y ARIMAC",
        "pregunta": "¿Dónde se deben respaldar los cuadros electrónicos?",
        "opciones": [
            "En el equipo generador y en otro equipo diferente",
            "Únicamente en el equipo generador",
            "Solo en la nube institucional",
            "En una memoria USB personal",
        ],
        "respuesta": 0,
        "explicacion": "Los cuadros electrónicos se deben respaldar en el equipo generador y en otro equipo diferente.",
    },
    {
        "tema": "II. Expediente Clínico y ARIMAC",
        "pregunta": "Entre otros documentos, ¿qué debe contener el expediente clínico?",
        "opciones": [
            "Solo las notas médicas del último año",
            "Historia clínica, resultados de laboratorio y gabinete, diagnósticos y plan de tratamiento",
            "Únicamente los consentimientos informados",
            "El comprobante de vigencia de derechos",
        ],
        "respuesta": 1,
        "explicacion": "El expediente debe contener: Historia Clínica, interrogatorio, exploración física, resultados de laboratorio y gabinete, diagnósticos, plan de tratamiento, hoja de enfermería, cartas de consentimiento informado, entre otros.",
    },
    {
        "tema": "II. Expediente Clínico y ARIMAC",
        "pregunta": "¿Qué documento del expediente registra la salida del paciente por decisión propia?",
        "opciones": [
            "Nota de defunción",
            "Hoja de enfermería",
            "Hoja de egreso voluntario",
            "Carta de consentimiento informado",
        ],
        "respuesta": 2,
        "explicacion": "La hoja de egreso voluntario documenta la salida del paciente por decisión propia y forma parte del expediente clínico.",
    },
    # --- SISTEMAS DE INFORMACIÓN (adicionales) ---
    {
        "tema": "III. Sistemas de Información en Salud",
        "pregunta": "¿En qué fecha se implantó el DataMart Estadísticas Médicas?",
        "opciones": [
            "Diciembre de 2002",
            "Enero de 2004",
            "Junio de 2005",
            "Enero de 2003",
        ],
        "respuesta": 1,
        "explicacion": "El DataMart Estadísticas Médicas fue desarrollado en 2003 y su implantación fue en enero de 2004.",
    },
    {
        "tema": "III. Sistemas de Información en Salud",
        "pregunta": "¿Cuáles son los módulos del DataMart Estadísticas Médicas?",
        "opciones": [
            "Captura de Formatos, Validación SIAIS/SIMO, Envío de Información y Administrador",
            "Consulta Externa, Hospitalización y Enlace",
            "Registro, Codificación y Cierre",
            "Urgencias, Laboratorio y Farmacia",
        ],
        "respuesta": 0,
        "explicacion": "Los módulos del DataMart son: Captura de Formatos, Validación SIAIS/SIMO, Envío de Información y Administrador.",
    },
    {
        "tema": "III. Sistemas de Información en Salud",
        "pregunta": "En las unidades de medicina familiar, ¿desde qué sistema se transfieren las consultas hacia el SIAIS?",
        "opciones": [
            "SIMO Central",
            "DataMart",
            "SIMF",
            "SEED",
        ],
        "respuesta": 2,
        "explicacion": "Las consultas se transfieren del SIMF (Sistema de Información de Medicina Familiar) al SIAIS, con el cual tiene interface.",
    },
    {
        "tema": "III. Sistemas de Información en Salud",
        "pregunta": "¿Qué dirección emite el SIMO Central y sus manuales de operación?",
        "opciones": [
            "DGIS",
            "DIS",
            "CIAE",
            "DIDT (Dirección de Innovación y Desarrollo Tecnológico)",
        ],
        "respuesta": 3,
        "explicacion": "El SIMO Central y sus manuales de operación son emitidos por la Dirección de Innovación y Desarrollo Tecnológico (DIDT).",
    },
    # --- VIGILANCIA EPIDEMIOLÓGICA (adicionales) ---
    {
        "tema": "IV. Vigilancia Epidemiológica",
        "pregunta": "¿Qué significan las siglas SUIVE?",
        "opciones": [
            "Sistema Único de Información para Vigilancia Epidemiológica",
            "Sistema Unificado de Vigilancia de Enfermedades",
            "Subsistema de Información de Vigilancia Estatal",
            "Servicio Único de Investigación y Vigilancia Epidemiológica",
        ],
        "respuesta": 0,
        "explicacion": "SUIVE = Sistema Único de Información para Vigilancia Epidemiológica.",
    },
    {
        "tema": "IV. Vigilancia Epidemiológica",
        "pregunta": "¿Con qué sistema se genera el Informe Semanal de Enfermedades Transmisibles y No Transmisibles?",
        "opciones": [
            "SIMO Central",
            "SIAIS",
            "SEED",
            "DataMart",
        ],
        "respuesta": 1,
        "explicacion": "El Informe Semanal de Enfermedades Transmisibles y No Transmisibles se genera con el SIAIS.",
    },
    {
        "tema": "IV. Vigilancia Epidemiológica",
        "pregunta": "En la nomenclatura BAEE00SS.DBF del archivo SUAVE, ¿qué representan las letras EE?",
        "opciones": [
            "El número de semana",
            "La clave de la unidad médica",
            "La clave del Estado",
            "El año del informe",
        ],
        "respuesta": 2,
        "explicacion": "En BAEE00SS.DBF, EE representa la clave del Estado y SS el número de la semana.",
    },
    {
        "tema": "IV. Vigilancia Epidemiológica",
        "pregunta": "En la nomenclatura BAEE00SS.DBF del archivo SUAVE, ¿qué representan las letras SS?",
        "opciones": [
            "La clave del Estado",
            "El turno de captura",
            "El código del padecimiento",
            "El número de la semana",
        ],
        "respuesta": 3,
        "explicacion": "En BAEE00SS.DBF, SS representa el número de la semana epidemiológica.",
    },
    {
        "tema": "IV. Vigilancia Epidemiológica",
        "pregunta": "¿Quién valida la información del Informe Semanal subida a la plataforma IBSv2?",
        "opciones": [
            "El Epidemiólogo",
            "El Director de la unidad",
            "El personal del ARIMAC",
            "La DIDT",
        ],
        "respuesta": 0,
        "explicacion": "Una vez subido el archivo a la plataforma IBSv2 Informe Semanal, se informa al Epidemiólogo para que valide la información.",
    },
    {
        "tema": "IV. Vigilancia Epidemiológica",
        "pregunta": "¿Para qué se utilizan los listados nominales en el ARIMAC?",
        "opciones": [
            "Para entregarlos a los pacientes",
            "Únicamente para corregir información",
            "Para publicarlos en la unidad",
            "Para enviarlos a la Secretaría de Salud",
        ],
        "respuesta": 1,
        "explicacion": "Los listados nominales solo se utilizan en el ARIMAC para corregir información.",
    },
    {
        "tema": "IV. Vigilancia Epidemiológica",
        "pregunta": "¿Qué genera el SUIVE respecto a los padecimientos del informe semanal?",
        "opciones": [
            "Certificados de defunción",
            "Cuadros de productividad",
            "Listados nominales de padecimientos de interés epidemiológico",
            "Recetas electrónicas",
        ],
        "respuesta": 2,
        "explicacion": "El SUIVE genera listados nominales de padecimientos del informe semanal y de padecimientos de interés epidemiológico.",
    },
    {
        "tema": "IV. Vigilancia Epidemiológica",
        "pregunta": "¿Cuál de los siguientes es un documento epidemiológico que debe resguardarse en el ARIMAC?",
        "opciones": [
            "El censo de personal de la unidad",
            "Los vales de almacén",
            "El inventario de equipo médico",
            "El Informe Semanal (previo-definitivo)",
        ],
        "respuesta": 3,
        "explicacion": "Entre los documentos a resguardar están: RAIS, notas médicas, el Informe Semanal (previo-definitivo) y los informes mensuales de productividad.",
    },
    # --- INDICADORES (adicionales) ---
    {
        "tema": "V. Indicadores Médicos",
        "pregunta": "¿Qué programas de salud integran los informes mensuales de coberturas?",
        "opciones": [
            "Salud del Niño, del Adolescente, de la Mujer, del Hombre y del Adulto Mayor",
            "Vacunación, Nutrición y Salud Bucal",
            "Prevención, Curación y Rehabilitación",
            "Materno-Infantil y Enfermedades Crónicas",
        ],
        "respuesta": 0,
        "explicacion": "Los informes mensuales de coberturas se integran por los programas: Salud del Niño, Salud del Adolescente, Salud de la Mujer, Salud del Hombre y Salud del Adulto Mayor.",
    },
    {
        "tema": "V. Indicadores Médicos",
        "pregunta": "¿Qué componentes incluye el Programa Salud del Niño en los informes de coberturas?",
        "opciones": [
            "Vacunación, Estimulación Temprana y Salud Bucal",
            "Nutrición, Prevención y Control, y Detección de Enfermedades",
            "Crecimiento, Desarrollo y Alimentación",
            "Peso, Talla y Agudeza Visual",
        ],
        "respuesta": 1,
        "explicacion": "El Programa Salud del Niño incluye: Nutrición, Prevención y Control, y Detección de Enfermedades.",
    },
    {
        "tema": "V. Indicadores Médicos",
        "pregunta": "Uno de los indicadores de atención médica mide el porcentaje de derechohabientes referidos a:",
        "opciones": [
            "Trabajo social",
            "Urgencias",
            "Segundo nivel de atención",
            "Medicina preventiva",
        ],
        "respuesta": 2,
        "explicacion": "El indicador mide el porcentaje de derechohabientes referidos a segundo nivel de atención.",
    },
    {
        "tema": "V. Indicadores Médicos",
        "pregunta": "¿Qué personal otorga la atención preventiva integrada a los derechohabientes?",
        "opciones": [
            "La enfermera",
            "El médico familiar",
            "El epidemiólogo",
            "El trabajador social",
        ],
        "respuesta": 0,
        "explicacion": "La atención preventiva integrada en derechohabientes es otorgada por la enfermera.",
    },
    {
        "tema": "V. Indicadores Médicos",
        "pregunta": "En planificación familiar, ¿cómo se registran las aceptantes?",
        "opciones": [
            "Por unidad médica y turno",
            "Por tipo de método anticonceptivo y grupo de edad",
            "Por número de hijos",
            "Por estado civil y ocupación",
        ],
        "respuesta": 1,
        "explicacion": "En planificación familiar las aceptantes se registran por Tipo de Método Anticonceptivo y Grupo de Edad.",
    },
    {
        "tema": "V. Indicadores Médicos",
        "pregunta": "En Salud en el Trabajo, ¿cómo se reportan los días de incapacidad por pacientes?",
        "opciones": [
            "Solo por riesgo de trabajo",
            "Solo por enfermedad general",
            "Por turno y categoría del trabajador",
            "Total, por enfermedad general y por riesgo de trabajo",
        ],
        "respuesta": 3,
        "explicacion": "Los días de incapacidad por pacientes se reportan en total, por enfermedad general y por riesgo de trabajo.",
    },
    {
        "tema": "V. Indicadores Médicos",
        "pregunta": "¿Según qué lista se reportan los motivos de atención que generaron días de incapacidad?",
        "opciones": [
            "La CIE-10 a 4 dígitos",
            "El catálogo CLUES",
            "La lista mexicana",
            "El catálogo de puestos del IMSS",
        ],
        "respuesta": 2,
        "explicacion": "El total de motivos de atención que generaron días de incapacidad se reporta por lista mexicana.",
    },
    {
        "tema": "V. Indicadores Médicos",
        "pregunta": "¿Qué aspectos comprende el informe de Salud Materna?",
        "opciones": [
            "Embarazo, puerperio y sus complicaciones; climaterio y menopausia; y vigilancia materna",
            "Solo el control prenatal",
            "Únicamente partos y cesáreas",
            "Lactancia materna y vacunación",
        ],
        "respuesta": 0,
        "explicacion": "Salud Materna comprende: embarazo, puerperio y sus complicaciones; climaterio y menopausia; y vigilancia materna.",
    },
    {
        "tema": "V. Indicadores Médicos",
        "pregunta": "En embarazadas, ¿qué mide uno de los indicadores de atención médica?",
        "opciones": [
            "El número de ultrasonidos realizados",
            "El porcentaje con auscultación de frecuencia cardiaca fetal",
            "El porcentaje con cesárea programada",
            "El número de consultas odontológicas",
        ],
        "respuesta": 1,
        "explicacion": "El indicador mide el porcentaje de embarazadas con auscultación de frecuencia cardiaca fetal.",
    },
    # --- CIE-10 (adicionales) ---
    {
        "tema": "VI. Clasificación Internacional de Enfermedades (CIE-10)",
        "pregunta": "¿Cuál es el rango de códigos CIE-10 del Capítulo X (Enfermedades del sistema respiratorio)?",
        "opciones": [
            "I00-I99",
            "E00-E90",
            "J00-J99",
            "P00-P96",
        ],
        "respuesta": 2,
        "explicacion": "El Capítulo X (Enfermedades del sistema respiratorio) corresponde a los códigos J00-J99.",
    },
    {
        "tema": "VI. Clasificación Internacional de Enfermedades (CIE-10)",
        "pregunta": "¿A qué capítulo de la CIE-10 corresponde el rango O00-O99?",
        "opciones": [
            "Cap. XVI: Afecciones del periodo perinatal",
            "Cap. XV: Embarazo, parto y puerperio",
            "Cap. XVII: Malformaciones congénitas",
            "Cap. XX: Causas externas",
        ],
        "respuesta": 1,
        "explicacion": "El rango O00-O99 corresponde al Capítulo XV: Embarazo, parto y puerperio.",
    },
    {
        "tema": "VI. Clasificación Internacional de Enfermedades (CIE-10)",
        "pregunta": "¿A qué corresponde el rango C00-D48 en la CIE-10?",
        "opciones": [
            "Neoplasias",
            "Enfermedades infecciosas y parasitarias",
            "Enfermedades del sistema circulatorio",
            "Enfermedades endocrinas y metabólicas",
        ],
        "respuesta": 0,
        "explicacion": "El rango C00-D48 corresponde al Capítulo II: Neoplasias.",
    },
    {
        "tema": "VI. Clasificación Internacional de Enfermedades (CIE-10)",
        "pregunta": "¿Qué paso de selección de mortalidad corresponde a 'Hay Secuencia' (antes R1)?",
        "opciones": [
            "SP2",
            "SP6",
            "SP8",
            "SP4",
        ],
        "respuesta": 3,
        "explicacion": "SP4 corresponde a 'Hay Secuencia' (antes conocida como Regla 1).",
    },
    {
        "tema": "VI. Clasificación Internacional de Enfermedades (CIE-10)",
        "pregunta": "¿Qué paso de selección de mortalidad corresponde a 'No Hay Secuencia' (antes R2)?",
        "opciones": [
            "SP4",
            "SP5",
            "SP7",
            "SP1",
        ],
        "respuesta": 1,
        "explicacion": "SP5 corresponde a 'No Hay Secuencia' (antes conocida como Regla 2).",
    },
    {
        "tema": "VI. Clasificación Internacional de Enfermedades (CIE-10)",
        "pregunta": "¿A qué corresponde el paso M2 en la codificación de mortalidad?",
        "opciones": [
            "Especificidad (antes RD)",
            "Asociación",
            "Causa Obvia",
            "Volver a comprobar pasos anteriores",
        ],
        "respuesta": 0,
        "explicacion": "M2 corresponde a Especificidad (antes conocida como Regla D).",
    },
    # --- MORTALIDAD (adicionales) ---
    {
        "tema": "VII. Mortalidad y Certificado de Defunción",
        "pregunta": "¿Qué contiene la Parte 1 del certificado de defunción?",
        "opciones": [
            "Los datos generales del fallecido",
            "La secuencia causal (a, b, c, d) desde la causa directa hasta la causa básica",
            "Los antecedentes familiares",
            "El nombre del médico certificante",
        ],
        "respuesta": 1,
        "explicacion": "La Parte 1 contiene la secuencia causal (líneas a, b, c, d) que va de la causa directa a la causa básica de defunción.",
    },
    {
        "tema": "VII. Mortalidad y Certificado de Defunción",
        "pregunta": "¿Qué se registra en la Parte 2 del certificado de defunción?",
        "opciones": [
            "La causa directa de la muerte",
            "Los datos del Registro Civil",
            "Otros estados patológicos significativos que contribuyeron a la muerte",
            "La secuencia causal completa",
        ],
        "respuesta": 2,
        "explicacion": "En la Parte 2 se registran otros estados patológicos significativos que contribuyeron a la muerte, pero que no forman parte de la secuencia causal.",
    },
    {
        "tema": "VII. Mortalidad y Certificado de Defunción",
        "pregunta": "¿Cuál es el objetivo principal de la codificación de la mortalidad?",
        "opciones": [
            "Obtener la causa básica de defunción",
            "Contar el número total de muertes",
            "Identificar al médico tratante",
            "Registrar la hora de la defunción",
        ],
        "respuesta": 0,
        "explicacion": "La causa básica de defunción es el objetivo principal de la codificación de la mortalidad.",
    },
    {
        "tema": "VII. Mortalidad y Certificado de Defunción",
        "pregunta": "¿Se acepta la hemofilia (D66, D67) como debida a cualquier otra enfermedad?",
        "opciones": [
            "Sí, siempre",
            "Solo si es hereditaria",
            "Sí, en adultos mayores",
            "No, es una secuencia rechazada",
        ],
        "respuesta": 3,
        "explicacion": "No se acepta la hemofilia (D66, D67) como debida a cualquier otra enfermedad. Es una secuencia rechazada.",
    },
    {
        "tema": "VII. Mortalidad y Certificado de Defunción",
        "pregunta": "¿Se acepta el suicidio (X60-X84) como debido a otras afecciones?",
        "opciones": [
            "Sí, si hay depresión diagnosticada",
            "No, es una secuencia rechazada",
            "Solo con dictamen del ministerio público",
            "Sí, en cualquier caso",
        ],
        "respuesta": 1,
        "explicacion": "No se acepta el suicidio (X60-X84) como debido a otras afecciones. Es una secuencia rechazada.",
    },
    {
        "tema": "VII. Mortalidad y Certificado de Defunción",
        "pregunta": "¿Qué indica el código O97.X?",
        "opciones": [
            "Muerte obstétrica de causa no especificada",
            "Muerte materna antes de los 42 días",
            "Muerte por secuela de causa obstétrica directa, un año o más después de la terminación del embarazo",
            "Muerte fetal tardía",
        ],
        "respuesta": 2,
        "explicacion": "O97.X: Muerte por secuela de causa obstétrica directa, que ocurre un año o más después de la terminación del embarazo.",
    },
    {
        "tema": "VII. Mortalidad y Certificado de Defunción",
        "pregunta": "¿Para qué se autoriza la presunción de causa intercurrente?",
        "opciones": [
            "Para aceptar una secuencia como fue informada, sin cambiar la codificación",
            "Para modificar la causa básica seleccionada",
            "Para eliminar causas de la Parte 2",
            "Para recodificar el certificado completo",
        ],
        "respuesta": 0,
        "explicacion": "La presunción de causa intercurrente se autoriza para aceptar una secuencia como fue informada; no se debe utilizar para cambiar la codificación.",
    },
    # --- PROCESOS OPERATIVOS (adicionales) ---
    {
        "tema": "VIII. Procesos Operativos del ARIMAC",
        "pregunta": "En el proceso de integración de información al DataMart, ¿quién codifica y captura la información?",
        "opciones": [
            "El Director de la unidad",
            "El personal del ARIMAC",
            "El médico familiar",
            "La DIDT",
        ],
        "respuesta": 1,
        "explicacion": "El ARIMAC es quien codifica y captura la información en el proceso de integración al DataMart.",
    },
    {
        "tema": "VIII. Procesos Operativos del ARIMAC",
        "pregunta": "Una vez confirmada la transferencia de información de las unidades, ¿qué se ejecuta?",
        "opciones": [
            "El respaldo semanal",
            "El cierre nacional",
            "El cierre delegacional",
            "La depuración de expedientes",
        ],
        "respuesta": 2,
        "explicacion": "Confirmada la transferencia de información de las unidades, se ejecuta el cierre delegacional. Después la DIS realiza el cierre nacional.",
    },
    {
        "tema": "VIII. Procesos Operativos del ARIMAC",
        "pregunta": "¿Qué subsistema del DataMart corresponde a 'Egresos Hospitalarios'?",
        "opciones": [
            "Subsistema 13",
            "Subsistema 10",
            "Subsistema 27",
            "Subsistema 31",
        ],
        "respuesta": 0,
        "explicacion": "El subsistema 13 corresponde a Egresos Hospitalarios (automatizado, generado por SIAIS/SIMO).",
    },
    {
        "tema": "VIII. Procesos Operativos del ARIMAC",
        "pregunta": "¿Qué subsistema del DataMart corresponde a 'Motivos de Demanda'?",
        "opciones": [
            "Subsistema 10",
            "Subsistema 13",
            "Subsistema 31",
            "Subsistema 27",
        ],
        "respuesta": 3,
        "explicacion": "El subsistema 27 corresponde a Motivos de Demanda (automatizado, generado por SIAIS/SIMO).",
    },
    {
        "tema": "VIII. Procesos Operativos del ARIMAC",
        "pregunta": "¿Quién actualiza los catálogos antes de cada cierre nacional?",
        "opciones": [
            "La CIAE",
            "La DIS",
            "El ARIMAC",
            "La UMAE",
        ],
        "respuesta": 1,
        "explicacion": "La DIS (División de Información en Salud) actualiza los catálogos antes de cada cierre nacional.",
    },
    {
        "tema": "VIII. Procesos Operativos del ARIMAC",
        "pregunta": "¿Quiénes son los responsables del análisis de la información en la unidad médica?",
        "opciones": [
            "El Director y la Jefatura de departamento clínico",
            "El personal del ARIMAC",
            "La Delegación",
            "El epidemiólogo y la enfermera",
        ],
        "respuesta": 0,
        "explicacion": "El Director y la Jefatura de departamento clínico de la unidad son los responsables del análisis de la información.",
    },
]


# ============================================================
# FLASHCARDS
# ============================================================

FLASHCARDS = [
    {"frente": "¿Qué es ARIMAC?", "reverso": "Área de Información Médica y Archivo Clínico"},
    {"frente": "¿Qué es CIAE?", "reverso": "Coordinación de Información y Análisis Estratégico"},
    {"frente": "¿Qué es OIMAC?", "reverso": "Oficina de Información Médica y Archivo Clínico (en UMAE)"},
    {"frente": "¿Qué es SIAIS?", "reverso": "Sistema de Información de Atención Integral a la Salud"},
    {"frente": "¿Qué es SIMO Central?", "reverso": "Sistema de Información Médico Operativo"},
    {"frente": "¿Qué es SIMF?", "reverso": "Sistema de Información de Medicina Familiar"},
    {"frente": "¿Qué es SEED?", "reverso": "Subsistema Epidemiológico y Estadístico de Defunciones"},
    {"frente": "¿Qué es SINAIS?", "reverso": "Sistema Nacional de Información en Salud"},
    {"frente": "¿Qué es CLUES?", "reverso": "Clave Única de Establecimientos de Salud"},
    {"frente": "¿Qué es DGIS?", "reverso": "Dirección General de Información en Salud"},
    {"frente": "¿Qué es SINAC?", "reverso": "Subsistema de Información sobre Nacimientos"},
    {"frente": "¿Qué es RAIS?", "reverso": "Registro de Actividades de Atención Integral de la Salud"},
    {"frente": "¿Qué es SUIVE?", "reverso": "Sistema Único de Información para Vigilancia Epidemiológica"},
    {"frente": "¿Qué es MAAGTIC?", "reverso": "Manual Administrativo de Aplicación General para las TIC"},
    {"frente": "¿Qué es DIS?", "reverso": "División de Información en Salud"},
    {"frente": "¿Qué es DIDT?", "reverso": "Dirección de Innovación y Desarrollo Tecnológico"},
    {"frente": "¿Qué es un DataMart EM?", "reverso": "Repositorio de hardware y software que almacena grandes volúmenes de datos para análisis y toma de decisiones"},
    {"frente": "¿Qué es un Data Warehouse?", "reverso": "Conjunto de DataMarts que mantienen las mismas características"},
    {"frente": "Nomenclatura del archivo SUAVE", "reverso": "BAEE00SS.DBF (EE=Estado, SS=Semana)"},
    {"frente": "Paso SP1 de mortalidad", "reverso": "Causa única en el Certificado"},
    {"frente": "Paso SP3 de mortalidad", "reverso": "Más de una línea usada en la Parte 1"},
    {"frente": "Paso SP6 de mortalidad", "reverso": "Causa Obvia"},
    {"frente": "Paso SP7 de mortalidad", "reverso": "Afecciones 'Mal Definidas'"},
    {"frente": "Paso SP8 de mortalidad", "reverso": "Afecciones 'Poco Probables de Causar la Muerte'"},
    {"frente": "Paso M1 de mortalidad", "reverso": "Asociación"},
    {"frente": "Paso M2 de mortalidad", "reverso": "Especificidad"},
    {"frente": "Paso M4 de mortalidad", "reverso": "Instrucciones sobre procedimientos médicos, envenenamiento, lesiones principales, muertes maternas"},
    {"frente": "Código O95.X", "reverso": "Muerte obstétrica de causa no especificada"},
    {"frente": "Código O96.X", "reverso": "Muerte materna por causa obstétrica después de 42 días pero antes de un año"},
    {"frente": "Código O97.X", "reverso": "Muerte por secuela de causa obstétrica directa, un año o más después"},
    {"frente": "NOM-035-SSA3-2012", "reverso": "Norma Oficial Mexicana en materia de Información en Salud"},
    {"frente": "Atributos de calidad (NOM-035)", "reverso": "Oportunidad, Cobertura, Integridad, Confiabilidad, Validez y Consistencia"},
    {"frente": "Módulos del SIMO Central", "reverso": "Consulta Externa, Hospitalización y Enlace"},
    {"frente": "Subsistemas automatizados del DataMart", "reverso": "10, 13, 27, 31, 32 (generados por SIAIS/SIMO)"},
    {"frente": "Tiempo mínimo de conservación del expediente clínico", "reverso": "5 años"},
    {"frente": "Formato diario en Medicina Familiar", "reverso": "RAIS (Registro de Actividades de Atención Integral de la Salud)"},
    {"frente": "Formatos de consulta externa de especialidades", "reverso": "4-30-6 y 4-30-6P/90"},
    {"frente": "Ley Federal de Archivos - fecha de publicación", "reverso": "23 de enero de 2012 en el DOF"},
    {"frente": "Plataforma del Informe Semanal", "reverso": "IBSv2 Informe Semanal"},
    {"frente": "Año de implantación del DataMart", "reverso": "Enero de 2004"},
]


# ============================================================
# INICIALIZACIÓN DEL ESTADO
# ============================================================

HISTORIAL_ARCHIVO = Path(__file__).parent / "historial_examenes.json"


def cargar_historial():
    try:
        with open(HISTORIAL_ARCHIVO, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return datos if isinstance(datos, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def guardar_historial(historial):
    try:
        with open(HISTORIAL_ARCHIVO, "w", encoding="utf-8") as f:
            json.dump(historial, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def init_state():
    defaults = {
        "pagina": "inicio",
        "quiz_activo": False,
        "quiz_preguntas": [],
        "quiz_idx": 0,
        "quiz_score": 0,
        "quiz_respondida": False,
        "quiz_seleccion": None,
        "quiz_tema": "Todos",
        "quiz_total": 10,
        "quiz_detalle": [],
        "quiz_guardado": False,
        "preguntas_usadas": [],
        "flashcard_idx": 0,
        "flashcard_mostrar": False,
        "flashcard_lista": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    if "historial" not in st.session_state:
        st.session_state.historial = cargar_historial()


init_state()


# ============================================================
# SIDEBAR - NAVEGACIÓN
# ============================================================

with st.sidebar:
    st.markdown("### 📊 Guía Interactiva")
    st.markdown("**Coordinador de Estadística**")
    st.markdown("IMSS - C.P. 05 - 2020")
    st.divider()

    paginas = {
        "inicio": "🏠 Inicio",
        "temas": "📚 Temas de Estudio",
        "quiz": "✏️ Examen de Práctica",
        "flashcards": "🃏 Tarjetas de Memorización",
        "glosario": "📖 Glosario de Siglas",
        "progreso": "📊 Mi Progreso",
    }

    for key, label in paginas.items():
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.pagina = key
            if key != "quiz":
                st.session_state.quiz_activo = False
            st.rerun()

    st.divider()
    st.caption("Material basado en el PDF oficial del IMSS - 3a Categoría Coordinador de Estadística 2020")


# ============================================================
# PÁGINAS
# ============================================================

def pagina_inicio():
    st.markdown("""
    <div class="main-header">
        <h1>📊 Guía Interactiva</h1>
        <p>Coordinador de Estadística - IMSS</p>
        <p>Material Didáctico C.P. 05 - 2020 | 3a Categoría</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Bienvenido a tu herramienta de estudio interactiva")
    st.markdown("Esta aplicación te ayudará a prepararte para el examen de la 3a categoría de **Coordinador de Estadística** del IMSS.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 📚 Temas de Estudio")
        st.markdown("Revisa el contenido organizado por temas y subtemas con la información clave del material didáctico.")
        if st.button("Ir a Temas", key="go_temas", use_container_width=True):
            st.session_state.pagina = "temas"
            st.rerun()

    with col2:
        st.markdown("#### ✏️ Examen de Práctica")
        st.markdown(f"Pon a prueba tus conocimientos con **{len(PREGUNTAS)} preguntas** de opción múltiple basadas en el material.")
        if st.button("Iniciar Examen", key="go_quiz", use_container_width=True):
            st.session_state.pagina = "quiz"
            st.rerun()

    with col3:
        st.markdown("#### 🃏 Tarjetas de Memorización")
        st.markdown(f"**{len(FLASHCARDS)} tarjetas** con las siglas, conceptos y datos más importantes para memorizar.")
        if st.button("Ver Tarjetas", key="go_flash", use_container_width=True):
            st.session_state.pagina = "flashcards"
            st.rerun()

    st.divider()

    st.markdown("### 📋 Contenido del Material")
    for tema, info in TEMAS.items():
        with st.expander(f"{info['icono']} {tema}"):
            st.markdown(f"*{info['descripcion']}*")
            for subtema in info["subtemas"]:
                st.markdown(f"- {subtema}")


def pagina_temas():
    st.markdown("""
    <div class="main-header">
        <h1>📚 Temas de Estudio</h1>
        <p>Contenido organizado del material didáctico</p>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs([f"{info['icono']} {tema.split('. ', 1)[-1][:25]}" for tema, info in TEMAS.items()])

    for tab, (tema, info) in zip(tabs, TEMAS.items()):
        with tab:
            st.markdown(f"### {info['icono']} {tema}")
            st.markdown(f"*{info['descripcion']}*")
            st.divider()

            for subtema, puntos in info["subtemas"].items():
                with st.expander(f"📌 {subtema}", expanded=False):
                    for punto in puntos:
                        st.markdown(f"- {punto}")


def pagina_quiz():
    st.markdown("""
    <div class="main-header">
        <h1>✏️ Examen de Práctica</h1>
        <p>Pon a prueba tus conocimientos</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.quiz_activo:
        # Configuración del examen
        st.markdown("### Configuración del Examen")

        conteo_por_tema = {t: sum(1 for p in PREGUNTAS if p["tema"] == t) for t in TEMAS}
        temas_disponibles = ["Todos"] + [t for t in TEMAS if conteo_por_tema[t] > 0]

        def etiqueta_tema(t):
            n = len(PREGUNTAS) if t == "Todos" else conteo_por_tema[t]
            return f"{t} ({n} preguntas)"

        tema_sel = st.selectbox("Selecciona el tema:", temas_disponibles, format_func=etiqueta_tema, key="quiz_tema_sel")

        indices_filtrados = [i for i, p in enumerate(PREGUNTAS) if tema_sel == "Todos" or p["tema"] == tema_sel]
        max_preguntas = len(indices_filtrados)

        if max_preguntas <= 5:
            num_preguntas = max_preguntas
        else:
            num_preguntas = st.slider(
                "Número de preguntas:",
                min_value=5,
                max_value=max_preguntas,
                value=min(10, max_preguntas),
                key="quiz_num_slider",
            )

        st.info(f"Se seleccionarán **{num_preguntas}** preguntas aleatorias de **{max_preguntas}** disponibles. Las preguntas no se repiten entre exámenes hasta agotar el banco del tema.")

        if st.button("🚀 Iniciar Examen", type="primary", use_container_width=True):
            # Evitar repetir preguntas ya usadas en exámenes anteriores:
            # primero entran las no vistas; solo se completa con vistas si no alcanzan
            usadas = set(st.session_state.preguntas_usadas)
            disponibles = [i for i in indices_filtrados if i not in usadas]
            if len(disponibles) >= num_preguntas:
                seleccion_idx = random.sample(disponibles, num_preguntas)
            else:
                faltantes = num_preguntas - len(disponibles)
                repetibles = [i for i in indices_filtrados if i in usadas]
                seleccion_idx = disponibles + random.sample(repetibles, faltantes)
                random.shuffle(seleccion_idx)
                # Se agotó el banco del tema: reiniciar su ciclo
                for i in indices_filtrados:
                    usadas.discard(i)
            usadas.update(seleccion_idx)
            st.session_state.preguntas_usadas = list(usadas)

            # Barajar el orden de las opciones de cada pregunta
            examen = []
            for i in seleccion_idx:
                p = PREGUNTAS[i]
                orden = list(range(len(p["opciones"])))
                random.shuffle(orden)
                examen.append({
                    "tema": p["tema"],
                    "pregunta": p["pregunta"],
                    "opciones": [p["opciones"][j] for j in orden],
                    "respuesta": orden.index(p["respuesta"]),
                    "explicacion": p["explicacion"],
                })

            st.session_state.quiz_preguntas = examen
            st.session_state.quiz_idx = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_activo = True
            st.session_state.quiz_respondida = False
            st.session_state.quiz_seleccion = None
            st.session_state.quiz_total = num_preguntas
            st.session_state.quiz_tema = tema_sel
            st.session_state.quiz_detalle = []
            st.session_state.quiz_guardado = False
            st.rerun()
    else:
        # Examen en curso
        preguntas = st.session_state.quiz_preguntas
        idx = st.session_state.quiz_idx

        if idx >= len(preguntas):
            # Resultados finales
            score = st.session_state.quiz_score
            total = st.session_state.quiz_total
            pct = (score / total) * 100

            st.markdown(f"""
            <div class="score-box">
                <h2>Resultado Final</h2>
                <h1>{score} / {total} ({pct:.0f}%)</h1>
                <p>{'¡Excelente! Dominas el material.' if pct >= 80 else '¡Buen esfuerzo! Sigue estudiando.' if pct >= 60 else 'Necesitas repasar más. ¡No te rindas!'}</p>
            </div>
            """, unsafe_allow_html=True)

            # Guardar en historial (solo una vez por examen)
            if not st.session_state.quiz_guardado:
                st.session_state.historial.append({
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "tema": st.session_state.quiz_tema,
                    "score": score,
                    "total": total,
                    "porcentaje": pct,
                    "detalle": st.session_state.quiz_detalle,
                })
                guardar_historial(st.session_state.historial)
                st.session_state.quiz_guardado = True

            st.markdown("")

            temas_fallados = sorted({d["tema"] for d in st.session_state.quiz_detalle if not d["acierto"]})
            if temas_fallados:
                st.markdown("### 💡 Temas a reforzar:")
                for t in temas_fallados:
                    st.markdown(f"- {t}")

            with st.expander("📋 Revisar mis respuestas"):
                for n, d in enumerate(st.session_state.quiz_detalle, 1):
                    icono = "✅" if d["acierto"] else "❌"
                    st.markdown(f"{icono} **{n}. {d['pregunta']}**")
                    if not d["acierto"]:
                        st.markdown(f"- Tu respuesta: {d['seleccion']}")
                        st.markdown(f"- Respuesta correcta: **{d['correcta']}**")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Nuevo Examen", use_container_width=True):
                    st.session_state.quiz_activo = False
                    st.rerun()
            with col2:
                if st.button("📚 Ir a Temas", use_container_width=True):
                    st.session_state.pagina = "temas"
                    st.session_state.quiz_activo = False
                    st.rerun()
            return

        pregunta = preguntas[idx]

        # Barra de progreso
        progreso = (idx) / len(preguntas)
        st.progress(progreso, text=f"Pregunta {idx + 1} de {len(preguntas)}")

        col_info, col_score = st.columns([3, 1])
        with col_info:
            st.caption(f"📁 {pregunta['tema']}")
        with col_score:
            st.caption(f"✅ Aciertos: {st.session_state.quiz_score}")

        st.markdown(f"### {pregunta['pregunta']}")

        if not st.session_state.quiz_respondida:
            for i, opcion in enumerate(pregunta["opciones"]):
                if st.button(opcion, key=f"opt_{idx}_{i}", use_container_width=True):
                    st.session_state.quiz_seleccion = i
                    st.session_state.quiz_respondida = True
                    if i == pregunta["respuesta"]:
                        st.session_state.quiz_score += 1
                    st.session_state.quiz_detalle.append({
                        "tema": pregunta["tema"],
                        "pregunta": pregunta["pregunta"],
                        "seleccion": pregunta["opciones"][i],
                        "correcta": pregunta["opciones"][pregunta["respuesta"]],
                        "acierto": i == pregunta["respuesta"],
                    })
                    st.rerun()
        else:
            seleccion = st.session_state.quiz_seleccion
            correcta = pregunta["respuesta"]

            for i, opcion in enumerate(pregunta["opciones"]):
                if i == correcta:
                    st.markdown(f'<div class="correct">✅ {opcion}</div>', unsafe_allow_html=True)
                elif i == seleccion and seleccion != correcta:
                    st.markdown(f'<div class="incorrect">❌ {opcion}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f"⬜ {opcion}")

            if seleccion == correcta:
                st.success("¡Correcto!")
            else:
                st.error("Incorrecto")

            st.markdown(f"""
            <div class="study-note">
                <strong>📝 Explicación:</strong> {pregunta['explicacion']}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("")
            if st.button("➡️ Siguiente Pregunta", type="primary", use_container_width=True):
                st.session_state.quiz_idx += 1
                st.session_state.quiz_respondida = False
                st.session_state.quiz_seleccion = None
                st.rerun()


def pagina_flashcards():
    st.markdown("""
    <div class="main-header">
        <h1>🃏 Tarjetas de Memorización</h1>
        <p>Repasa siglas, conceptos y datos clave</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.flashcard_lista:
        st.session_state.flashcard_lista = list(range(len(FLASHCARDS)))
        random.shuffle(st.session_state.flashcard_lista)

    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 2, 1])
    with col_ctrl2:
        st.markdown(f"**Tarjeta {st.session_state.flashcard_idx + 1} de {len(FLASHCARDS)}**")

    idx_real = st.session_state.flashcard_lista[st.session_state.flashcard_idx]
    card = FLASHCARDS[idx_real]

    # Tarjeta
    st.markdown(f"""
    <div class="flashcard-front">
        <div>{card['frente']}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("👁️ Mostrar / Ocultar Respuesta", use_container_width=True, key="flip"):
            st.session_state.flashcard_mostrar = not st.session_state.flashcard_mostrar

    if st.session_state.flashcard_mostrar:
        st.markdown(f"""
        <div class="flashcard-back">
            <div><strong>{card['reverso']}</strong></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    col_prev, col_shuffle, col_next = st.columns(3)

    with col_prev:
        if st.button("⬅️ Anterior", use_container_width=True, key="prev_card"):
            if st.session_state.flashcard_idx > 0:
                st.session_state.flashcard_idx -= 1
                st.session_state.flashcard_mostrar = False
                st.rerun()

    with col_shuffle:
        if st.button("🔀 Mezclar", use_container_width=True, key="shuffle_cards"):
            random.shuffle(st.session_state.flashcard_lista)
            st.session_state.flashcard_idx = 0
            st.session_state.flashcard_mostrar = False
            st.rerun()

    with col_next:
        if st.button("➡️ Siguiente", use_container_width=True, key="next_card"):
            if st.session_state.flashcard_idx < len(FLASHCARDS) - 1:
                st.session_state.flashcard_idx += 1
                st.session_state.flashcard_mostrar = False
                st.rerun()

    # Progreso visual
    st.progress((st.session_state.flashcard_idx + 1) / len(FLASHCARDS))


def pagina_glosario():
    st.markdown("""
    <div class="main-header">
        <h1>📖 Glosario de Siglas</h1>
        <p>Referencia rápida de todas las siglas del material</p>
    </div>
    """, unsafe_allow_html=True)

    glosario = {
        "ARIMAC": "Área de Información Médica y Archivo Clínico",
        "CIAE": "Coordinación de Información y Análisis Estratégico",
        "CIE-10": "Clasificación Internacional de Enfermedades, 10a Revisión",
        "CIF": "Clasificación Internacional del Funcionamiento, de la Discapacidad y de la Salud",
        "CIE-MC": "Clasificación Internacional de Enfermedades - Modificación Clínica",
        "CLUES": "Clave Única de Establecimientos de Salud",
        "CVE": "Coordinación de Vigilancia Epidemiológica",
        "DGIS": "Dirección General de Información en Salud",
        "DIDT": "Dirección de Innovación y Desarrollo Tecnológico",
        "DIS": "División de Información en Salud",
        "DOF": "Diario Oficial de la Federación",
        "IBSv2": "Plataforma del Informe Semanal (versión 2)",
        "IMSS": "Instituto Mexicano del Seguro Social",
        "MAAGTIC": "Manual Administrativo de Aplicación General para las TIC",
        "MMIM": "Manual Metodológico de Indicadores Médicos",
        "NOM": "Norma Oficial Mexicana",
        "OIMAC": "Oficina de Información Médica y Archivo Clínico (en UMAE)",
        "RAIS": "Registro de Actividades de Atención Integral de la Salud",
        "SEED": "Subsistema Epidemiológico y Estadístico de Defunciones",
        "SIAIS": "Sistema de Información de Atención Integral a la Salud",
        "SIMF": "Sistema de Información de Medicina Familiar",
        "SIMO": "Sistema de Información Médico Operativo",
        "SINAC": "Subsistema de Información sobre Nacimientos",
        "SINAIS": "Sistema Nacional de Información en Salud",
        "SNS": "Sistema Nacional de Salud",
        "SUIVE": "Sistema Único de Información para Vigilancia Epidemiológica",
        "TIC": "Tecnologías de la Información y la Comunicación",
        "UMAE": "Unidad Médica de Alta Especialidad",
        "UMF": "Unidad de Medicina Familiar",
    }

    buscar = st.text_input("🔍 Buscar sigla o significado:", key="buscar_glosario")

    for sigla, significado in sorted(glosario.items()):
        if buscar:
            term = buscar.upper()
            if term not in sigla.upper() and term not in significado.upper():
                continue
        st.markdown(f"""
        <div class="tema-card">
            <strong>{sigla}</strong>: {significado}
        </div>
        """, unsafe_allow_html=True)


def pagina_progreso():
    st.markdown("""
    <div class="main-header">
        <h1>📊 Mi Progreso</h1>
        <p>Historial de exámenes realizados</p>
    </div>
    """, unsafe_allow_html=True)

    historial = st.session_state.historial

    if not historial:
        st.info("Aún no has realizado ningún examen. ¡Ve a la sección de Examen de Práctica para comenzar!")
        if st.button("✏️ Ir al Examen", use_container_width=True):
            st.session_state.pagina = "quiz"
            st.rerun()
        return

    # Estadísticas generales
    total_examenes = len(historial)
    mejor = max(h["porcentaje"] for h in historial)
    promedio = sum(h["porcentaje"] for h in historial) / total_examenes
    ultimo = historial[-1]["porcentaje"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Exámenes Realizados", total_examenes)
    col2.metric("Mejor Calificación", f"{mejor:.0f}%")
    col3.metric("Promedio", f"{promedio:.0f}%")
    col4.metric("Último Examen", f"{ultimo:.0f}%")

    st.divider()

    # Tabla de historial
    st.markdown("### Historial de Exámenes")
    st.caption("Toca un examen para revisar tus respuestas.")
    for i, h in enumerate(reversed(historial), 1):
        num = total_examenes - i + 1
        emoji = "🟢" if h["porcentaje"] >= 80 else "🟡" if h["porcentaje"] >= 60 else "🔴"
        tema = h.get("tema", "Todos")
        with st.expander(f"{emoji} Examen {num} | {h['fecha']} | {h['score']}/{h['total']} ({h['porcentaje']:.0f}%) | {tema}"):
            detalle = h.get("detalle", [])
            if not detalle:
                st.caption("Este examen no tiene detalle de respuestas guardado.")
            else:
                falladas = [d for d in detalle if not d["acierto"]]
                if falladas:
                    temas_fallados = sorted({d["tema"] for d in falladas})
                    st.markdown("**Temas a reforzar:** " + ", ".join(temas_fallados))
                for n, d in enumerate(detalle, 1):
                    icono = "✅" if d["acierto"] else "❌"
                    st.markdown(f"{icono} **{n}. {d['pregunta']}**")
                    if not d["acierto"]:
                        st.markdown(f"- Tu respuesta: {d['seleccion']}")
                        st.markdown(f"- Respuesta correcta: **{d['correcta']}**")

    st.divider()

    if st.button("🗑️ Limpiar historial", use_container_width=True):
        st.session_state.historial = []
        guardar_historial([])
        st.rerun()


# ============================================================
# ROUTER
# ============================================================

router = {
    "inicio": pagina_inicio,
    "temas": pagina_temas,
    "quiz": pagina_quiz,
    "flashcards": pagina_flashcards,
    "glosario": pagina_glosario,
    "progreso": pagina_progreso,
}

pagina_actual = st.session_state.get("pagina", "inicio")
router.get(pagina_actual, pagina_inicio)()
