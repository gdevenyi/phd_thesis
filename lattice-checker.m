function abcf = lattice_checker(film_file, substrate_file)
%Lattice Checker Program, inputs two files of lists of names, crystal groups and lattice constants, and outpus fixes within tol mistmach
%Written by Gabriel A. Devenyi
%August 10, 2013
tol = 8;
%command_line=argv();
%film_file = command_line(1,1);
%substrate_file = command_line(2,1);


fid = fopen (substrate_file, 'r');
i = 1;
sub_name = char(zeros(10,100));
sub_type = char(zeros(1,100));

while (~feof(fid))
    [a, sub_type(i), sub_a(i), sub_c(i)] = fscanf (fid, '%s %s %f %f', 'C');
    sub_name(i,1:length(a)) = a;
    i=i+1;
end

fclose (fid);

fid = fopen (film_file, 'r');
i = 1;
film_name = char(zeros(10,100));
film_type = char(zeros(1,100));

while (~feof(fid))
    [a, film_type(i), film_a(i), film_c(i)] = fscanf (fid, '%s %s %f %f', 'C');
    film_name(i,1:length(a)) = a;
    i = i + 1;
end

fclose (fid);
disp(sprintf('Film,Symmetry,Substrate,Symmetry,Mismatch(%%),Rounded Ratio,Original Ratio'));
%Iterate through Substrates
for i=1:length(sub_a)
    
    %Iterate through Films
    for j=1:length(film_a)
        if (strtrim(film_name(j,:)) == strtrim(sub_name(i,:)))
            continue;
        end
        %Cubic on Cubic Check
        if (film_type(j) == 'C' && sub_type(i) == 'C')
            original_ratio = sub_a(i)/film_a(j);
            
            if (original_ratio < 1)
                ratio = 1/round(1/original_ratio);
            else
                ratio = round(original_ratio);
            end
            
            %(sub_a(i) - ratio*film_a(j))/(ratio*film_a(j)) * 100;
            (ratio*film_a(j) - sub_a(i)) / sub_a(i) *100;
            if (abs(ans) < tol)
                disp(sprintf('%s,C,%s,C,%g,%g,%g',strtrim(film_name(j,:)), strtrim(sub_name(i,:)), ans, ratio, original_ratio));
            end
        end
        
        %Cubic on Hexagonal
        if (film_type(j) == 'C' && sub_type(i) == 'H')
            original_ratio = sub_a(i)/(film_a(j)*sqrt(2));
            
            if (original_ratio < 1);
                ratio = 1/round(1/original_ratio);
            else
                ratio = round(original_ratio);
            end
            
            %(sub_a(i) - ratio*film_a(j)*sqrt(2))/(ratio*film_a(j)*sqrt(2)) * 100;
            (ratio*film_a(j)*sqrt(2) - sub_a(i)) / sub_a(i) * 100;
            if (abs(ans) < tol)
                disp(sprintf('%s,C,%s,H,%g,%g,%g',strtrim(film_name(j,:)), strtrim(sub_name(i,:)), ans, ratio, original_ratio));
            end
        end
        
        %Tetragonal on Cubic Check
        if (film_type(j) == 'T' && sub_type(i) == 'C')
            original_ratio = sub_a(i)/film_a(j);
            
            if (original_ratio < 1)
                ratio = 1/round(1/original_ratio);
            else
                ratio = round(original_ratio);
            end
            
            %(sub_a(i) - ratio*film_a(j))/(ratio*film_a(j)) * 100;
            (ratio*film_a(j) - sub_a(i)) / sub_a(i) *100;
            if (abs(ans) < tol)
                disp(sprintf('%s,T,%s,C,%g,%g,%g',strtrim(film_name(j,:)), strtrim(sub_name(i,:)), ans, ratio, original_ratio));
            end
        end
        
        %Hexagonal on Hexagonal Check
        if (film_type(j) == 'H' && sub_type(i) == 'H')
            original_ratio = sub_a(i)/film_a(j);
            
            if (original_ratio < 1)
                ratio = 1/round(1/original_ratio);
            else
                ratio = round(original_ratio);
            end
            
            %(sub_a(i) - ratio*film_a(j))/(ratio*film_a(j)) * 100;
            (ratio*film_a(j) - sub_a(i)) / sub_a(i) *100;
            if (abs(ans) < tol)
                disp(sprintf('%s,H,%s,H,%g,%g,%g',strtrim(film_name(j,:)), strtrim(sub_name(i,:)), ans, ratio, original_ratio));
            end
        end
        
        %Hexagonal on Cubic Check
        if (film_type(j) == 'H' && sub_type(i) == 'C')
            original_ratio = (sub_a(i)*sqrt(2))/film_a(j);
            
            if (original_ratio < 1)
                ratio = 1/round(1/original_ratio);
            else
                ratio = round(original_ratio);
            end
            
            %(sub_a(i)*sqrt(2) - ratio*film_a(j))/(ratio*film_a(j)) * 100;
            (ratio*film_a(j) - sub_a(i)*sqrt(2))/(sub_a(i)*sqrt(2)) * 100;
            if (abs(ans) < tol)
                disp(sprintf('%s,H,%s,C,%g,%g,%g',strtrim(film_name(j,:)), strtrim(sub_name(i,:)), ans, ratio, original_ratio));
            end
        end
        
        %Cubic on Tetragonal Check
        if (film_type(j) == 'C' && sub_type(i) == 'T')
            original_ratio = (sub_a(i))/film_a(j);
            
            if (original_ratio < 1)
                ratio = 1/round(1/original_ratio);
            else
                ratio = round(original_ratio);
            end
            
            (sub_a(i) - ratio*film_a(j))/(ratio*film_a(j)) * 100;
            if (abs(ans) < tol)
                disp(sprintf('%s,C,%s,T,%g,%g,%g',strtrim(film_name(j,:)), strtrim(sub_name(i,:)), ans, ratio, original_ratio));
            end
        end
        
        %Tetragonal on Tetragonal Check
        if (film_type(j) == 'T' && sub_type(i) == 'T')
            original_ratio = (sub_a(i))/film_a(j);
            
            if (original_ratio < 1)
                ratio = 1/round(1/original_ratio);
            else
                ratio = round(original_ratio);
            end
            
            %(sub_a(i) - ratio*film_a(j))/(ratio*film_a(j)) * 100;
            (ratio*film_a(j) - sub_a(i)) / sub_a(i) *100;
            if (abs(ans) < tol)
                disp(sprintf('%s,T,%s,T,%g,%g,%g',strtrim(film_name(j,:)), strtrim(sub_name(i,:)), ans, ratio, original_ratio));
            end
        end
    end
    
end
