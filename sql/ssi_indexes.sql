CREATE INDEX pdb_index ON public.moe USING btree ("PDB");
CREATE INDEX pdb_cb_index ON public.moe USING btree ("PDB", "cb.cb");
CREATE INDEX cb_type_index ON public.moe USING btree ("Type", "cb.cb");
CREATE INDEX pdb_type_idx ON public.moe USING btree ("PDB", "Type");
CREATE INDEX moe_residue_1_idx ON public.moe USING btree ("substring"("Residue.1", 6, 3));
CREATE INDEX moe_residue_2_idx ON public.moe USING btree ("substring"("Residue.2", 6, 3));
CREATE INDEX residue_pair_cb_idx ON public.moe USING btree ("substring"("Residue.1", 6, 3), "substring"("Residue.2", 6, 3), "cb.cb");
CREATE INDEX host_lower_idx ON public.moe USING btree (lower("expressionHost"));
CREATE INDEX source_lower_idx ON public.moe USING btree (lower(source));
