--
-- PostgreSQL database dump
--

\restrict PM6om1X30y55VIiasW2cqBuPw7C4AJHz5fLOmClLFdjHIRO8w8K31a7teDxHm5f

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

-- Started on 2026-03-02 11:14:42

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 222 (class 1259 OID 25039)
-- Name: marques; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.marques (
    id_marques integer NOT NULL,
    nom_marques character varying(100) NOT NULL
);


ALTER TABLE public.marques OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 25038)
-- Name: marques_id_marques_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.marques ALTER COLUMN id_marques ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.marques_id_marques_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 220 (class 1259 OID 25031)
-- Name: materials; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.materials (
    id_materials integer NOT NULL,
    type_materials character varying(10) NOT NULL,
    density numeric(4,2)
);


ALTER TABLE public.materials OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 25030)
-- Name: materials_id_materials_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.materials ALTER COLUMN id_materials ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.materials_id_materials_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 224 (class 1259 OID 25047)
-- Name: spools; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.spools (
    id_spools integer NOT NULL,
    nfc_id character varying(255) NOT NULL,
    id_materials integer NOT NULL,
    id_marques integer NOT NULL,
    color_name character varying(100),
    initial_weight numeric(5,1) DEFAULT 1000,
    empty_spool_weight integer,
    diametre numeric(4,2) DEFAULT 1.75 NOT NULL,
    temperature_imp numeric(4,1) DEFAULT 0,
    temperature_table numeric(4,1) DEFAULT 0,
    debit numeric(4,1) DEFAULT 0,
    pressure_advance numeric(4,3) DEFAULT 0,
    vit_volum_max integer DEFAULT 10,
    vit_imp numeric DEFAULT 0
);


ALTER TABLE public.spools OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 25046)
-- Name: spools_id_spools_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.spools ALTER COLUMN id_spools ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.spools_id_spools_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 226 (class 1259 OID 25074)
-- Name: usage_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usage_logs (
    id_usage_logs integer NOT NULL,
    weight_used numeric(5,1) DEFAULT 0.0 NOT NULL,
    print_date date,
    id_spools integer NOT NULL,
    project_name character varying(255)
);


ALTER TABLE public.usage_logs OWNER TO postgres;

--
-- TOC entry 5052 (class 0 OID 0)
-- Dependencies: 226
-- Name: TABLE usage_logs; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.usage_logs IS 'historique de consomation';


--
-- TOC entry 225 (class 1259 OID 25073)
-- Name: usage_logs_id_usage_logs_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.usage_logs ALTER COLUMN id_usage_logs ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.usage_logs_id_usage_logs_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 5042 (class 0 OID 25039)
-- Dependencies: 222
-- Data for Name: marques; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.marques (id_marques, nom_marques) FROM stdin;
1	CC3D
2	CREALITY CR SERIES
3	Polymaker
4	PrintomaxMax3D
5	PrintoMax3D
6	dfqf
7	hdkfqlfq
8	ggsgd
9	sfdf
10	Esun
11	Eryone
\.


--
-- TOC entry 5040 (class 0 OID 25031)
-- Dependencies: 220
-- Data for Name: materials; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.materials (id_materials, type_materials, density) FROM stdin;
9	PLA-Bois	\N
10	Nylon (PA)	\N
5	ABS	1.04
1	PLA	1.25
2	PETG	1.27
3	PLA+ PRO	1.25
4	PLA+	1.25
6	TPU	1.21
7	ASA	1.07
8	PLA CF	1.30
13	Galaxy PLA	\N
12	ePLA-Magic	1.25
\.


--
-- TOC entry 5044 (class 0 OID 25047)
-- Dependencies: 224
-- Data for Name: spools; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spools (id_spools, nfc_id, id_materials, id_marques, color_name, initial_weight, empty_spool_weight, diametre, temperature_imp, temperature_table, debit, pressure_advance, vit_volum_max, vit_imp) FROM stdin;
1	04:54:B4:AC:7A:26:81	1	1	Rose	1025.0	169	1.75	0.0	0.0	0.0	0.000	0	0
2	04:DB:BF:AC:7A:26:81	1	2	Multicolor gradient	1013.0	169	1.75	0.0	0.0	0.0	0.000	0	0
3	04:BF:C6:AC:7A:26:81	1	3	Bleu saphir	822.0	152	1.75	0.0	0.0	0.0	0.000	0	0
4	04:D1:CC:AC:7A:26:81	3	4	Pure White	796.0	152	1.75	0.0	0.0	0.0	0.000	0	0
5	04:C3:D3:AC:7A:26:81	1	3	Bleu saphir	384.0	152	1.75	0.0	0.0	0.0	0.000	0	0
6	04:B6:DF:AC:7A:26:81	4	5	Sky blue	1053.0	169	1.75	0.0	0.0	0.0	0.000	0	0
7	04:C6:E6:AC:7A:26:81	3	5	Fruity apple	984.0	152	1.75	0.0	0.0	0.0	0.000	0	0
11	04:16:ED:AC:7A:26:81	12	10	Dark twinkling gold	1011.0	152	1.75	0.0	0.0	0.0	0.000	0	0
12	04:B1:F7:AC:7A:26:81	13	11	Sirius Nebula	1024.0	152	1.75	0.0	0.0	0.0	0.000	0	0
13	04:CB:FD:AC:7A:26:81	12	10	Dark twinkling purple	1019.0	152	1.75	0.0	0.0	0.0	0.000	0	0
14	04:22:15:AC:7A:26:81	3	5	Fruity Melon	1003.0	169	1.75	0.0	0.0	0.0	0.000	0	0
\.


--
-- TOC entry 5046 (class 0 OID 25074)
-- Dependencies: 226
-- Data for Name: usage_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usage_logs (id_usage_logs, weight_used, print_date, id_spools, project_name) FROM stdin;
\.


--
-- TOC entry 5053 (class 0 OID 0)
-- Dependencies: 221
-- Name: marques_id_marques_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.marques_id_marques_seq', 11, true);


--
-- TOC entry 5054 (class 0 OID 0)
-- Dependencies: 219
-- Name: materials_id_materials_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.materials_id_materials_seq', 13, true);


--
-- TOC entry 5055 (class 0 OID 0)
-- Dependencies: 223
-- Name: spools_id_spools_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.spools_id_spools_seq', 14, true);


--
-- TOC entry 5056 (class 0 OID 0)
-- Dependencies: 225
-- Name: usage_logs_id_usage_logs_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usage_logs_id_usage_logs_seq', 15, true);


--
-- TOC entry 4883 (class 2606 OID 25045)
-- Name: marques marques_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.marques
    ADD CONSTRAINT marques_pkey PRIMARY KEY (id_marques);


--
-- TOC entry 4881 (class 2606 OID 25037)
-- Name: materials materials_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materials
    ADD CONSTRAINT materials_pkey PRIMARY KEY (id_materials);


--
-- TOC entry 4886 (class 2606 OID 25062)
-- Name: spools spools_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spools
    ADD CONSTRAINT spools_pkey PRIMARY KEY (id_spools);


--
-- TOC entry 4888 (class 2606 OID 25082)
-- Name: usage_logs usage_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usage_logs
    ADD CONSTRAINT usage_logs_pkey PRIMARY KEY (id_usage_logs);


--
-- TOC entry 4884 (class 1259 OID 25093)
-- Name: spools_id_spools_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX spools_id_spools_idx ON public.spools USING btree (id_spools, nfc_id, id_materials, id_marques, color_name, initial_weight, empty_spool_weight, diametre, temperature_imp, temperature_table, debit, pressure_advance, vit_volum_max, vit_imp);


--
-- TOC entry 4889 (class 2606 OID 25068)
-- Name: spools spools_id_marques_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spools
    ADD CONSTRAINT spools_id_marques_fkey FOREIGN KEY (id_marques) REFERENCES public.marques(id_marques);


--
-- TOC entry 4890 (class 2606 OID 25063)
-- Name: spools spools_id_materials_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.spools
    ADD CONSTRAINT spools_id_materials_fkey FOREIGN KEY (id_materials) REFERENCES public.materials(id_materials);


--
-- TOC entry 4891 (class 2606 OID 25083)
-- Name: usage_logs usage_logs_id_spools_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usage_logs
    ADD CONSTRAINT usage_logs_id_spools_fkey FOREIGN KEY (id_spools) REFERENCES public.spools(id_spools);


-- Completed on 2026-03-02 11:14:42

--
-- PostgreSQL database dump complete
--

\unrestrict PM6om1X30y55VIiasW2cqBuPw7C4AJHz5fLOmClLFdjHIRO8w8K31a7teDxHm5f

