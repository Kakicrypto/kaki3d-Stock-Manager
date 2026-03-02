-- =============================================
-- KAKI3D Stock Manager - Import Supabase
-- =============================================

-- 1. CREATION DES TABLES
-- =============================================

CREATE TABLE public.marques (
    id_marques integer NOT NULL,
    nom_marques character varying(100) NOT NULL
);

ALTER TABLE public.marques ALTER COLUMN id_marques ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.marques_id_marques_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public.materials (
    id_materials integer NOT NULL,
    type_materials character varying(10) NOT NULL,
    density numeric(4,2)
);

ALTER TABLE public.materials ALTER COLUMN id_materials ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.materials_id_materials_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

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

ALTER TABLE public.spools ALTER COLUMN id_spools ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.spools_id_spools_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

CREATE TABLE public.usage_logs (
    id_usage_logs integer NOT NULL,
    weight_used numeric(5,1) DEFAULT 0.0 NOT NULL,
    print_date date,
    id_spools integer NOT NULL,
    project_name character varying(255)
);

COMMENT ON TABLE public.usage_logs IS 'historique de consomation';

ALTER TABLE public.usage_logs ALTER COLUMN id_usage_logs ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.usage_logs_id_usage_logs_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

-- 2. CONTRAINTES ET CLES PRIMAIRES
-- =============================================

ALTER TABLE ONLY public.marques
    ADD CONSTRAINT marques_pkey PRIMARY KEY (id_marques);

ALTER TABLE ONLY public.materials
    ADD CONSTRAINT materials_pkey PRIMARY KEY (id_materials);

ALTER TABLE ONLY public.spools
    ADD CONSTRAINT spools_pkey PRIMARY KEY (id_spools);

ALTER TABLE ONLY public.usage_logs
    ADD CONSTRAINT usage_logs_pkey PRIMARY KEY (id_usage_logs);

-- 3. CLES ETRANGERES
-- =============================================

ALTER TABLE ONLY public.spools
    ADD CONSTRAINT spools_id_marques_fkey FOREIGN KEY (id_marques) REFERENCES public.marques(id_marques);

ALTER TABLE ONLY public.spools
    ADD CONSTRAINT spools_id_materials_fkey FOREIGN KEY (id_materials) REFERENCES public.materials(id_materials);

ALTER TABLE ONLY public.usage_logs
    ADD CONSTRAINT usage_logs_id_spools_fkey FOREIGN KEY (id_spools) REFERENCES public.spools(id_spools);

-- 4. INDEX
-- =============================================

CREATE INDEX spools_id_spools_idx ON public.spools USING btree (id_spools, nfc_id, id_materials, id_marques, color_name, initial_weight, empty_spool_weight, diametre, temperature_imp, temperature_table, debit, pressure_advance, vit_volum_max, vit_imp);

-- 5. DONNEES - MARQUES
-- =============================================

INSERT INTO public.marques (id_marques, nom_marques) OVERRIDING SYSTEM VALUE VALUES
(1, 'CC3D'),
(2, 'CREALITY CR SERIES'),
(3, 'Polymaker'),
(4, 'PrintomaxMax3D'),
(5, 'PrintoMax3D'),
(6, 'dfqf'),
(7, 'hdkfqlfq'),
(8, 'ggsgd'),
(9, 'sfdf'),
(10, 'Esun'),
(11, 'Eryone');

-- 6. DONNEES - MATERIALS
-- =============================================

INSERT INTO public.materials (id_materials, type_materials, density) OVERRIDING SYSTEM VALUE VALUES
(1, 'PLA', 1.25),
(2, 'PETG', 1.27),
(3, 'PLA+ PRO', 1.25),
(4, 'PLA+', 1.25),
(5, 'ABS', 1.04),
(6, 'TPU', 1.21),
(7, 'ASA', 1.07),
(8, 'PLA CF', 1.30),
(9, 'PLA-Bois', NULL),
(10, 'Nylon (PA)', NULL),
(12, 'ePLA-Magic', 1.25),
(13, 'Galaxy PLA', NULL);

-- 7. DONNEES - SPOOLS
-- =============================================

INSERT INTO public.spools (id_spools, nfc_id, id_materials, id_marques, color_name, initial_weight, empty_spool_weight, diametre, temperature_imp, temperature_table, debit, pressure_advance, vit_volum_max, vit_imp) OVERRIDING SYSTEM VALUE VALUES
(1,  '04:54:B4:AC:7A:26:81', 1,  1,  'Rose',                  1025.0, 169, 1.75, 0.0, 0.0, 0.0, 0.000, 0, 0),
(2,  '04:DB:BF:AC:7A:26:81', 1,  2,  'Multicolor gradient',   1013.0, 169, 1.75, 0.0, 0.0, 0.0, 0.000, 0, 0),
(3,  '04:BF:C6:AC:7A:26:81', 1,  3,  'Bleu saphir',            822.0, 152, 1.75, 0.0, 0.0, 0.0, 0.000, 0, 0),
(4,  '04:D1:CC:AC:7A:26:81', 3,  4,  'Pure White',             796.0, 152, 1.75, 0.0, 0.0, 0.0, 0.000, 0, 0),
(5,  '04:C3:D3:AC:7A:26:81', 1,  3,  'Bleu saphir',            384.0, 152, 1.75, 0.0, 0.0, 0.0, 0.000, 0, 0),
(6,  '04:B6:DF:AC:7A:26:81', 4,  5,  'Sky blue',              1053.0, 169, 1.75, 0.0, 0.0, 0.0, 0.000, 0, 0),
(7,  '04:C6:E6:AC:7A:26:81', 3,  5,  'Fruity apple',           984.0, 152, 1.75, 0.0, 0.0, 0.0, 0.000, 0, 0),
(11, '04:16:ED:AC:7A:26:81', 12, 10, 'Dark twinkling gold',   1011.0, 152, 1.75, 0.0, 0.0, 0.0, 0.000, 0, 0),
(12, '04:B1:F7:AC:7A:26:81', 13, 11, 'Sirius Nebula',         1024.0, 152, 1.75, 0.0, 0.0, 0.0, 0.000, 0, 0),
(13, '04:CB:FD:AC:7A:26:81', 12, 10, 'Dark twinkling purple', 1019.0, 152, 1.75, 0.0, 0.0, 0.0, 0.000, 0, 0),
(14, '04:22:15:AC:7A:26:81', 3,  5,  'Fruity Melon',          1003.0, 169, 1.75, 0.0, 0.0, 0.0, 0.000, 0, 0);

-- 8. REMISE A ZERO DES SEQUENCES
-- =============================================

SELECT pg_catalog.setval('public.marques_id_marques_seq', 11, true);
SELECT pg_catalog.setval('public.materials_id_materials_seq', 13, true);
SELECT pg_catalog.setval('public.spools_id_spools_seq', 14, true);
SELECT pg_catalog.setval('public.usage_logs_id_usage_logs_seq', 15, true);
