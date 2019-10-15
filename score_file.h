#include <list>
#include <string>
#include <stdlib.h>
#include <fstream>
typedef struct stru s;
struct stru
{
    string names;
    int scores;
};

int *read_score_file(string file_name)
{
    ifstream score_file;
    score_file.open(file_name);
    string line;
    list<s> player_list;
    while (score_file >> line)
    {
        int len = line.length();
        line = line.substr(1, len - 2);
        len = line.length();
        int pos = line.find(",");
        names.push_back(line.substr(7, pos));

        scores.push_back(atoi(line.substr(pos+6,len-1).c_str())));

        
    }
    return
}