% ToDo
% normalizzare a un numero preciso l'asse Y
% ingrandire la legenda
% creare immagini per ogni tipo di risultato
% dare nome agli assi?

path_begin = 'C:\Users\kivid\Dropbox\Universita\Corsi Magistrale\Modelli probabilistici per le decisioni\Progetto Mispelling\HMMispelling\results\performance\';

p_dataset = 'apple';
p_tweets = '_tweets';
p_autowrong = 'autowrong';
p_vitebimode = 'words';
p_corrected = '_corrected__';
p_transition = 'transition=';
p_training = 'Hybrid';
p_distribution = 'PseudoUniform';
p_keyprob = 'key-prob=';
p_eval = 'word';
p_evalstatic = '_evaluation_index.txt';
p_us = '_';

path_namefile = strcat(p_dataset, p_tweets, p_us, p_autowrong, p_us, p_vitebimode, p_corrected, p_transition, p_training, p_us, p_distribution, p_us, p_keyprob);
path = strcat(path_begin, path_namefile);
path_end = strcat(p_us, p_eval, p_evalstatic);

freq_table = zeros(5, 19);
col = 1;

for var = 0.05:0.05:0.95
    
    p_var = num2str(var);
    path_plusvar = strcat(path, p_var);
    path_final = strcat(path_plusvar, path_end);
    
    freq_table = import_errors_data(path_final, freq_table, col);
    
    col = col + 1;
    
end

x =  linspace(0,1,19);
y1 = freq_table(1,:);
y2 = freq_table(2,:);
y3 = freq_table(3,:);
y4 = freq_table(4,:);
y5 = freq_table(5,:);

if(strcmp(p_training, 'Hybrid'))
    p_trainingT = 'custom';
end

figure
plot(x,y1,x,y2,x,y3,x,y4,x,y5,'LineWidth',3);
legend('Perturbed - Corrected - Not true','Perturbed - Not corrected - Not true','Not perturbed - Corrected - Not true','Not perturbed - Not corrected - True','Perturbed - Corrected - True');
title(['Dataset: ', p_dataset, ' - Viterbi mode: ', p_vitebimode, ' - Training set: ', p_trainingT, ' - Emission probability: ', p_distribution]);