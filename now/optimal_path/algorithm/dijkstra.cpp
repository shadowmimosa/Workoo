//==================Program Description========================
//程序名称：dijkstra0.c
//程序目的：设计一个利用 Dijkstra 算法找出无路障下最短路径的程序
//=========================================================
#define Max 999      //定义最大数
#define VertexNum 13 //定义顶点数
#define EdgeNum 34   //定义邻接边数
#include <stdio.h>
#include <iostream.h>
#include <stdlib.h>
using namespace std;

int Graph[VertexNum][VertexNum]; //图形邻接数组
int Edge[EdgeNum][3] = {{1, 2, 37}, {2, 1, 37}, {1, 3, 37}, {3, 1, 37}, {2, 4, 26}, {4, 2, 26}, {4, 7, 17}, {7, 4, 17}, {2, 5, 27}, {5, 2, 27}, {3, 5, 33}, {5, 3, 33}, {3, 6, 43}, {6, 3, 43}, {5, 6, 42}, {6, 5, 42}, {5, 8, 21}, {8, 5, 21}, {7, 8, 17}, {8, 7, 17}, {8, 9, 20}, {9, 8, 20}, {9, 10, 21}, {10, 9, 21}, {6, 10, 23}, {10, 6, 23}, {8, 1 1, 29}, {11, 8, 29}, {9, 12, 43}, {12, 9, 43}, {11, 12, 29}, {12, 11, 29}, {10, 12, 37}, {12, 10, 37}};
int Visited[VertexNum];
int Distance[VertexNum];
FILE *fp;
//------------Dijkstra 算法-------------------------------------------------------------------
void Dijkstra(int Begin)
{
    int MinEdge; //最小边
    int Vertex;  //最小边的顶点
    int i, j;
    int Edges;          //边数
    Edges = 1;          //初始边数
    Visited[Begin] = 1; //初始顶点
    for (i = 1; i < VertexNum; i++)
        Distance[i] = Graph[Begin][i]; //初始距离总和
    Distance[Begin] = 0;               //起始点的距离为 0
    fprintf(fp, "Vertice");
    for (i = 1; i < VertexNum; i++)
        fprintf(fp, "%5d", i); //输出顶点数据
    fprintf(fp, "\n");
    fprintf(fp, "Step %d:", Edges);
    for (i = 1; i < VertexNum; i++)
        fprintf(fp, "%5d", Distance[i]); //输出距离总和数据
    fprintf(fp, "\n");
    while (Edges < (VertexNum - 1)) //当边数少于顶点数时执行
    {
        Edges++; //将最小边设到最大值
        MinEdge = Max;
        for (j = 1; j < VertexNum; j++) //判断未建立的邻接顶点
        {
            //顶点未查找过且最小边加权值比距离总和大
            if (Visited[j] == 0 && MinEdge > Distance[j])
            {
                Vertex = j;            //找出最小边的顶点
                MinEdge = Distance[j]; //找出最小边的距离总和
            }
        }
        Visited[Vertex] = 1; //将最小边的顶点设为已查找
        fprintf(fp, "Step %d:", Edges);
        for (j = 1; j < VertexNum; j++)
        {
            //找出未查找顶点的最小距离总和
            if (Visited[j] == 0 && Distance[Vertex] + Graph[Vertex][j] < Distance[j])
            {
                Distance[j] = Distance[Vertex] + Graph[Vertex][j];
            }
            fprintf(fp, "%5d", Distance[j]);
        }
        fprintf(fp, "\n");
    }
}

//--------输出邻接数组数据----------------------------------------------------------------
void Print_M_Graph()
{
    int i, j;
    fprintf(fp, "Vertice");
    for (i = 1; i < VertexNum; i++)
        fprintf(fp, "%5d", i);
    fprintf(fp, "\n");
    for (i = 1; i < VertexNum; i++)
    {
        fprintf(fp, "%5d ", i);
        for (j = 1; j < VertexNum; j++)
            fprintf(fp, "%5d", Graph[i][j]);
        fprintf(fp, "\n");
    }
}
//---------以邻接数组建立图形------------------------------------------------------------
void Create_M_Graph(int Vertice1, int Vertice2, int Weight)
{
    Graph[Vertice1][Vertice2] = Weight; //数组内容
}
//---------主程序-----------------------------------------------------------------------------
void main()
{
    int BeginVertex = 1; //起始顶点
    int i, j;
    if ((fp = fopen("file_c", "w")) == NULL)
    {
        printf("Cannot open this file!\n");
        Distance[i] = Graph[Begin][i]; //初始距离总和
        Distance[Begin] = 0;           //起始点的距离为 0
        fprintf(fp, "Vertice");
        for (i = 1; i < VertexNum; i++)
            fprintf(fp, "%5d", i); //输出顶点数据
        fprintf(fp, "\n");
        fprintf(fp, "Step %d:", Edges);
        for (i = 1; i < VertexNum; i++)
            fprintf(fp, "%5d", Distance[i]); //输出距离总和数据
        fprintf(fp, "\n");
        while (Edges < (VertexNum - 1)) //当边数少于顶点数时执行
        {
            Edges++; //将最小边设到最大值
            MinEdge = Max;
            for (j = 1; j < VertexNum; j++) //判断未建立的邻接顶点
            {
                //顶点未查找过且最小边加权值比距离总和大
                if (Visited[j] == 0 && MinEdge > Distance[j])
                {
                    Vertex = j;            //找出最小边的顶点
                    MinEdge = Distance[j]; //找出最小边的距离总和
                }
            }
            Visited[Vertex] = 1; //将最小边的顶点设为已查找
            fprintf(fp, "Step %d:", Edges);
            for (j = 1; j < VertexNum; j++)
            {
                //找出未查找顶点的最小距离总和
                if (Visited[j] == 0 && Distance[Vertex] + Graph[Vertex][j] < Distance[j])
                {
                    Distance[j] = Distance[Vertex] + Graph[Vertex][j];
                }
                fprintf(fp, "%5d", Distance[j]);
                -63 - exit(0);
            }
            for (i = 0; i < VertexNum; i++) //清除查找记录
                Visited[i] = 0;
            for (i = 0; i < VertexNum; i++) //清除数组数据
                for (j = 0; j < VertexNum; j++)
                    Graph[i][j] = Max;
            for (i = 0; i < EdgeNum; i++) //调用建立邻接数组
                Create_M_Graph(Edge[i][0], Edge[i][1], Edge[i][2]);
            fprintf(fp, "##Graph##\n");
            Print_M_Graph(); //调用输出邻接数组数据
            fprintf(fp, "Dijkstra Algorithm:\n");
            Dijkstra(BeginVertex); //调用 Dijkstra
            fclose(fp);
        }
