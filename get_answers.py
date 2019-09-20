import os
import sys
import operator

def ranking_answers(file_path, result_path):
    print("getting answer")
    queries = []
    scores = []
    with open(file_path) as f:
        for _, line in enumerate(f.readlines()):
            if _ == 0: continue
            line = line.strip().split('\t')
            queries.append((line[1], line[3]))

    with open(result_path) as f:
        for line in f.readlines():
            scores.append(float(line.split('\t')[1]))
    
    answers = dict(zip(queries, scores))
    print(sum(answers.values())/len(answers))
    answers = sorted(answers.items(), key=operator.itemgetter(1), reverse=True)
    # with open('answers.tsv', "w") as f:
    #     for answer in answers:
    #         f.write("{}\t{}\t{}\n".format(answer[0][0], answer[1], answer[0][1]))
    return answers

if __name__ == '__main__':
    ranking_answers(sys.argv[1], sys.argv[2])
