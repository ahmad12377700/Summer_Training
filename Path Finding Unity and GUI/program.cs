using System;
using System.IO;

public class Program
{
    static Graph g;
    static string dst;
    static Node dst_node;
    static C_List new_c = null;
    static Player_Loc loc = null;
    static C_node ptr = null;

    public static void Main(string[] args)
    {
        g = new Graph();
        new_c = new C_List();

        Console.WriteLine("Enter the path to the text file:");
        string path = Console.ReadLine();

        Console.WriteLine("Enter the destination node:");
        dst = Console.ReadLine();

        Initi_Graph(path);

        if (dst_node != null)
        {
            get_Path();
        }
        else
        {
            Console.WriteLine("Destination node does not exist.");
        }
    }

    static void Initi_Graph(string filePath)
    {
        try
        {
            using (StreamReader sr = new StreamReader(filePath))
            {
                string str;
                string[] arr;
                Node nd;

                while ((str = sr.ReadLine()) != null)
                {
                    if (str.Contains("%"))
                        break;

                    arr = str.Split(':');
                    nd = new Node(arr[0], float.Parse(arr[1]), float.Parse(arr[2]));
                    g.Insert_Node(nd);
                }

                while ((str = sr.ReadLine()) != null)
                {
                    if (str.Contains("%"))
                        continue;

                    arr = str.Split(':');
                    Node n_s = g.search_Node(arr[0]);
                    Node n_d = g.search_Node(arr[1]);
                    if (n_s != null && n_d != null)
                    {
                        float weight = float.Parse(arr[2]);
                        Link l = new Link(n_d, weight);
                        if (n_s.c_l == null)
                            n_s.c_l = new Connection_List(l);
                        else
                            n_s.c_l.Inser_Link(l);
                    }
                }
            }

            dst_node = g.search_Node(dst);
        }
        catch (Exception e)
        {
            Console.WriteLine("Error reading file: " + e.Message);
        }
    }

    static void get_Path()
    {
        loc = new Player_Loc(0, 0);  // Replace with actual starting coordinates
        O_List o_lst = new O_List();
        C_List c_lst = new C_List();
        Node nearest = g.get_Nearest(loc);
        O_node current = null;

        if (nearest != null)
        {
            current = o_lst.Add_node(nearest);
            current.nd.Add_Fanout(o_lst, c_lst);
        }

        c_lst.Add_node(current.nd);
        o_lst.Remove_node(current);

        while (o_lst.head != null && current.nd != dst_node)
        {
            current = o_lst.Lowest_cost();
            current.nd.Add_Fanout(o_lst, c_lst);
            c_lst.Add_node(current.nd);
            o_lst.Remove_node(current);
        }

        C_List c = g.get_path_nodes(dst_node);
        C_node pt = c.head;

        while (pt != null)
        {
            new_c.Add_node(pt.nd);
            pt = pt.next;
        }

        new_c.optimize_path(loc);

        // Print the path
        pt = new_c.head;
        while (pt != null)
        {
            Console.WriteLine(pt.nd.name);
            pt = pt.next;
        }
    }
}
