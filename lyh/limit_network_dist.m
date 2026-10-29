clear all;
m1 = 3;    %非饱和节点每次加入的边数
m2 = 1;    %非饱和节点每次删除的边数
m3 = 3;    %饱和节点每次加入的边数
m4 = 1;    %饱和节点每次删除的边数
m0 =  3;   %初始的顶点个数
N = 100;  %时间步 总共节点
K=10;%限制度
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
%加入的节点为 A(new) , 与其连接的点为old     生成 A(new ， old)
for new = m0+1:N
    oldlist=[];
    degree_a=[];
    degree_b=[];
    new
    
    %old vertice 速度越大连接上的概率越大
    Degree = sum(A(1:new-1,1:new-1))  %每个顶点的总度数
    Pi=Degree.*(K-Degree)
    %----------找正pi最小值-------------------
    alist=find(Degree(1:new-1)<K)%非饱和节点序列
    for i=1:length(alist)
        degree_a(i)=Degree(alist(i))
    end
    Pi_a=degree_a.*(K-degree_a)
    min_pi=min(Pi_a)
    %-----------------------------------------
    position=find(Pi<=0);%用正最小值替换负数节点的pi值
    position
    for i=1:length(position)
        Pi(position(i))=min_pi;  %一开始写的Degree 好像写错了
    end
    %----------------------------------
    
    blist=find(Degree(1:new-1)>=K);%饱和节点序列
    for i=1:length(blist)
        degree_b(i)=Degree(blist(i));
    end
    
    Pi_b=-(degree_b+1).*(K-degree_b-1)
    %n_a=length(alist);
    n_b=length(blist);
    %制造出一个pi的分布区间，模拟概率
    PiInterval(1) = Pi(1);
    for i=2:new-1
        PiInterval(i) = Pi(i)+PiInterval(i-1);
    end
    %连接 新节点 与 m个old节点
    Allpi = sum(Pi); %整个图的总pi
    
    %b同理
    if isempty(Pi_b)==0
        PiInterval_b(1) = Pi_b(1);
        if length(blist)>1
            for i=2:length(blist)
                PiInterval_b(i) = Pi_b(i)+PiInterval_b(i-1);
            end
        end
        Allpi_b = sum(Pi_b);
    end
    %全部节点增
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
    
    %饱和节点减
    if isempty(Pi_b)==0
        Pi_b=Pi_b/Allpi_b%减的概率
        for i = 1:length(blist)
           while 1
               if ismember(oldlist,blist(i)==1)%已经加过，不再减
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
                break;
             else
                 break;
             end
            % if A(cutnode,old) == 1
             %   oldlist(i)=old;
              %  A(cutnode,old) = 0;
               % A(old,cutnode) = 0;
                %break;
             %end
           end
        end
    end
    %饱和节点增
   % for i = 1:m3 
    %   while 1
     %    Ans  = fix(n*rand()+1); %要与度区间包含RandDegree的顶点相连
         %找到 符合 要求的区间所属顶点
      %   old = Ans;
       %  if ismember(oldlist_b,old)== 0%必须
        %    neighbour = A(:,old);
         %   cutnode  = fix(length(neighbour)*rand()+1)
          %  A(cutnode,old) = 1;
           % A(old,cutnode) = 1;
            %break;
         %end
       %end
    %end
    
    %求度分布
end
Degree = sum(A)  %完成后的网络的每个节点的度  2 3 2 2 4 3
UniDegree = unique(Degree);  %去重后度       2 3 4
length(UniDegree)
DegreeNum=zeros(1,length(UniDegree))
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