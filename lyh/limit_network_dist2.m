clear all;
m1 = 3;    %非饱和节点每次加入的边数
m2 = 1;    %非饱和节点每次删除的边数
m3 = 3;    %饱和节点每次加入的边数
m0 =  3;   %初始的顶点个数
N = 1000;  %时m4 = 1;    %饱和节点每次删除的边数
K=40;%限制度
C=1;%常数
%创建邻接矩阵    全0，无边
A = sparse(N,N);
%随机连边  1表示有边
for i=1:m0
    for j= (i+1):m0
        A(i,j)= round(rand());
        A(j,i) =  A(i,j);
    end
end   %初始完成
n=m0;%节点个数
A
Degree = sum(A(1:m0,1:m0))
Pi=Degree.*(K-Degree);
%degree_a=[];
%degree_b=[];
PiInterval(1) = Pi(1);
%PiInterval
for i=2:m0
    PiInterval(i) = Pi(i)+PiInterval(i-1);
end
    %连接 新节点 与 m个old节点
Allpi = sum(Pi); %整个图的总pi
%old vertice 速度越大连接上的概率越大

    %-----------------------------------------
    
    %b同理
    %if isempty(Pi_b)==0
    %    PiInterval_b(1) = Pi_b(1);
    %    if length(blist)>1
    %        for i=2:length(blist)
    %            PiInterval_b(i) = Pi_b(i)+PiInterval_b(i-1);
    %        end
    %    end
    %    Allpi_b = sum(Pi_b);
    %end
%加入的节点为 A(new) , 与其连接的点为old     生成 A(new ， old)

degree_b=[];
degree_a=[];
for new = m0+1:N
    new
    oldlist=[];
    blist=find(Degree(1:new-1)>=K);%饱和节点序列
    for i=1:length(blist)
        degree_b(i)=Degree(blist(i));
    end
    Pi_b=-(degree_b+1).*(K-degree_b-1);
    Allpi_b = sum(Pi_b);
    Allpi = PiInterval(new-1);
    %第new个节点增的过程
    olds=[];
    for i = 1:m1
       while 1
 %以概率从old节点中找到合适的顶点连接
         Randpi  = fix(Allpi*rand()+1); %要与度区间包含RandDegree的顶点相连
         %找到 符合 要求的区间所属顶点
         Ans = find(Randpi <= PiInterval(1:new-1));
         old = Ans(1);
         if A(new,old) == 0
            oldlist(i)=old;
            A(new,old) = 1;
            A(old,new) = 1;
            olds(i)=old;
            break;
         end
       end
    end
    %非饱和节点减
    %for i = 1:m2 
     %  while 1
      %   Ans  = fix(n_a*rand()+1); %要与度区间包含RandDegree的顶点相连
         %找到 符合 要求的区间所属顶点
       %  old = Ans;
        % if ismember(oldlist_a,old)== 0
         %   neighbour = A(:,old);
          %  cutnode  = fix(length(neighbour)*rand()+1)
           % A(cutnode,old) = 0;
           % A(old,cutnode) = 0;
           % break;
         %end
       %end
    %end
    blist_cut=[];
    cutnodes=[];
    %饱和节点减
    if isempty(Pi_b)==0
        Pi_b=Pi_b/Allpi_b;%减的概率
        for i = 1:length(blist)
           while 1
               if ismember(oldlist,blist(i))==1%已经加过，不再减
                   break;
               end
     %以概率从old节点中找到合适的顶点连接
             %Randpi  = fix(Allpi_b*rand()+1); %要与度区间包含RandDegree的顶点相连
             %找到 符合 要求的区间所属顶点
             %Ans = blist(find(Randpi <= PiInterval_b(1:new-1)));
             %old = Ans(1);
               if rand()<=Pi_b(i)
                  neighbour = find(A(:,blist(i))==1)
                  cutnode = neighbour(fix(length(neighbour)*rand()+1))
                  A(cutnode,old) = 0;
                  A(old,cutnode) = 0;
                  blist_cut=[blist_cut blist(i)];
                  cutnodes=[cutnodes cutnode];
                  break;
               else
                  break;
               end
           end
            % if A(cutnode,old) == 1
             %   oldlist(i)=old;
              %  A(cutnode,old) = 0;
               % A(old,cutnode) = 0;
                %break;
             %end
        end
    end
    
    Degree(new)=m1;
    Pi(new)=m1*(K-m1);
    PiInterval(new)=PiInterval(new-1)+Pi(new);
   
    alist=find(Degree(1:new)<K&Degree(1:new)>0);%非饱和节点序列
    for i=1:length(alist)
        degree_a(i)=Degree(alist(i));
    end
    Pi_a=degree_a.*(K-degree_a);
    min_pi=min(Pi_a)
    
    for i = 1:m1
        olds(i)
        pre=Degree(olds(i));
        Degree(olds(i))=Degree(olds(i))+1;
        if Degree(olds(i))>=K
            PiInterval(olds(i):new)=PiInterval(olds(i):new)+min_pi-pre*(K-pre);
        else
            PiInterval(olds(i):new)=PiInterval(olds(i):new)+Degree(olds(i))*(K-Degree(olds(i)))-pre*(K-pre);
        end
    end
    if isempty(Pi_b)==0
        for i = 1:length(blist_cut)
            pre=Degree(blist_cut(i));
            Degree(blist_cut(i))=Degree(blist_cut(i))-1;
            PiInterval(blist_cut(i):new)=PiInterval(blist_cut(i):new)+Degree(blist_cut(i))*(K-Degree(blist_cut(i)))-pre*(K-pre);
        end
        for i = 1:length(cutnodes)
            pre=Degree(cutnodes(i));
            Degree(cutnodes(i))=Degree(cutnodes(i))-1;
            PiInterval(cutnodes(i):new)=PiInterval(cutnodes(i):new)+Degree(cutnodes(i))*(K-Degree(cutnodes(i)))-pre*(K-pre);
        end
    end
    %已算好度区间，现在算Pi区间，把上面的增1改为Pi的
end
    
    
    %求度分布
Degree = sum(A)  %完成后的网络的每个节点的度  2 3 2 2 4 3
UniDegree = unique(Degree);  %去重后度       2 3 4
length(UniDegree);
DegreeNum=zeros(1,length(UniDegree));
for i = 1:length(UniDegree)
    DegreeNum(i) = sum(Degree==UniDegree(i));
end
UniDegree
DegreeNum
    %画图
   figure
   plot(UniDegree, DegreeNum ./ sum(DegreeNum),'.','markersize',18)
   xlabel('k'),ylabel('P(k)')
   hold on;
   x = min(UniDegree):max(UniDegree);
   y = 2 * m1^2 * x .^ ( -3 ); 
   py=1-2 * m1^2*(x.^(-2));
   plot( x , y , 'r' ) ; 
   legend('Simulation results','theoretical results');
   figure
   loglog(UniDegree, DegreeNum ./ sum(DegreeNum),'.','markersize',18)
   hold on;
   loglog( x , y , 'r' ) ;
   legend('Simulation results','theoretical results');
   %hold on;
   %plot(x,py,'r')
   %G=graph(A);
   %plot(G,'r');