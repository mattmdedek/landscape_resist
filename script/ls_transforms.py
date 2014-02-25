import glob
import os

class sample_mapper:

    def __init__(self, sample_map_fp, array_map_fp):
        """
        Takes a sample mapping file, tab separated, containing 'Species', 'Site', 'Array' and 'Sample' headers
        """
        if not os.path.isfile(sample_map_fp):
            raise Exception (sample_map_fp + " is not a file")

        if not os.path.isfile(array_map_fp):
            raise Exception (array_map_fp + " is not a file")

        self.dict_specimen_to_site = {}
        self.dict_object_id_to_site = {}
        self.sample_map_fp = sample_map_fp
        self.array_map_fp = array_map_fp
        self.__load_sample_map()
        self.__load_array_map()

    def __load_sample_map(self):
        """
        Parse the sample map file generate dictionary lookups used internally
        """
        self.dict_specimen_to_site.clear()
        with open(self.sample_map_fp) as f:
            flines = f.readlines()
        flines = [line.rstrip() for line in flines]
        fbody = [line.split("\t") for line in flines]
        
        header = fbody.pop(0)
        sample_idx = header.index('Sample')
        s_array_idx = header.index('Array')
        # if you want to get more mapping out of the sample file, do it here and add a dictionary to the class
        for specimen in fbody:
            self.dict_specimen_to_site[specimen[sample_idx]] = specimen[s_array_idx]

    def __load_array_map(self):
        """
        Takes an array ID file, comma separated, with a minimum of OBJECTID and array headers
        returns a dictionary with the OBJECTID as the key and the array as the value, used to
        interperet resistance matrix files.
        """

        self.dict_object_id_to_site.clear()
        with open(self.array_map_fp) as f:
            flines = f.readlines()
        flines = [line.rstrip() for line in flines]
        fbody = [line.split(',') for line in flines]
        
        header = fbody.pop(0)
        header = [tok.strip('"') for tok in header]
        id_idx = header.index('OBJECTID')
        array_idx = header.index('array')

        for l in fbody:
            self.dict_object_id_to_site[int(l[id_idx].strip('"'))] = l[array_idx].strip('"')

    def resist_to_matrix_file(self, fp_input, fp_output, sample_list):
        """
        Takes a matrix input file and converts to square matrix and saves for R 
        """

        resist = {}

        with open(fp_input) as f:
            flines = f.readlines()

        flines = [line.rstrip() for line in flines]
        fbody = [line.split(" ") for line in flines]

        for l in fbody:
            arr1 = self.dict_object_id_to_site[int(float(l[0]))]
            arr2 = self.dict_object_id_to_site[int(float(l[1]))]
            d = float(l[2])

            if not arr1 in resist:
                resist[arr1] = {}
                resist[arr1][arr1] = 0.0

            if not arr2 in resist:
                resist[arr2] = {}
                resist[arr2][arr2] = 0.0

            resist[arr1][arr2] = d
            resist[arr2][arr1] = d

        flines = []
        for s1 in sample_list:
            fline = []
            s1arr = self.specimen_to_site(s1)
            for s2 in sample_list:
                s2arr = self.specimen_to_site(s2)
                fline.append(str(resist[s1arr][s2arr]))
            flines.append("\t".join(fline))

        with open(fp_output, 'w') as of:
            outbody = of.write("\n".join(flines))

    def genetic_to_matrix_file(self, fp_input, fp_output):
        """
        Takes an input file saves it in the form need by R and returns a list of the sample Ids in the order recieved
        """

        with open(fp_input) as f:
            flines = f.readlines()

        flines = [line.rstrip() for line in flines]
        fbody = [line.split("\t") for line in flines]

        gene_dist = {}

        header = fbody.pop(0)
        header.pop(0)
        for h in header:
            gene_dist[h] = {}
            gene_dist[h][h] = '0.00000'

        line_no = 0
        for l in fbody:
            r_id = l[0]
            expected_col = header.index(r_id)
            if expected_col != line_no:
                raise RuntimeError("Mismatched row and column headers in " + fp_input + " at line number " + str(line_no))
            else:
                for c in range(1, len(l)):
                    d = l[c]
                    c_id = header[c - 1]
                    gene_dist[r_id][c_id] = d
                    gene_dist[c_id][r_id] = d
                #l.pop(0)
                #for t in l:
                #    out_toks.append(t)

            line_no = line_no + 1
            # out_lines.append("\t".join(out_toks))

        out_lines = []
        for h1 in header:
            out_tok = []
            for h2 in header:
                out_tok.append(gene_dist[h1][h2])
            out_lines.append("\t".join(out_tok))

        with open(fp_output, 'w') as of:
            of.write("\n".join(out_lines)) 
        header.pop(0)
        return header

    def euclid_to_matrix_file(self, fp_input, fp_output, sample_list):
        """
        Takes PairwiseEuclideanDistance file and saves matrix for R

        File is csv, header has quotes around fields, but this function won't allow bullshit commas in header titles
        """
        with open(fp_input) as f:
            flines = f.readlines()
        flines = [line.rstrip() for line in flines]
        fbody = [line.split(',') for line in flines]
        
        # remove double quotes from the header
        header = [t.strip('"') for t in fbody.pop(0)]

        f1idx = header.index("INPUT_FID")
        f2idx = header.index("NEAR_FID")
        didx = header.index("DISTANCE")

        dict_euc = {}
        for l in fbody:
            f1 = l[f1idx]
            f2 = l[f2idx]
            d = l[didx]

            if not f1 in dict_euc:
                dict_euc[f1] = {}
                dict_euc[f1][f1] = '0.00'

            if not f2 in dict_euc:
                dict_euc[f2] = {}
                dict_euc[f2][f2] = '0.00'

            dict_euc[f1][f2] = d

        out_lines = []
        for s1 in sample_list:
            le = []
            site1 = self.specimen_to_site(s1)
            for s2 in sample_list:
                site2 = self.specimen_to_site(s2)
                le.append(dict_euc[site1][site2])

            out_lines.append("\t".join(le))

        with open(fp_output, 'w') as of:
             of.write("\n".join(out_lines))

    def specimen_to_site(self, specimen):
        return self.dict_specimen_to_site[specimen]

