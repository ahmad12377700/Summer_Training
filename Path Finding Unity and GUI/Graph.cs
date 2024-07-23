using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using OpenCover.Framework.Model;
using Unity.VisualScripting;
using UnityEngine;
public class Graph 
{
    public Node head = null;
    public Node tail = null;
    public Graph() 
    { 
        head = null; 
        tail = null; 
    }
    public Node search_Node(string nd_name)
    {
        Node nd = null;
        Node nod = head;
        while (nod != null)
        {
            if (nod.name.Trim() == nd_name.Trim())
            {
                nd = nod;
                break;
            }
            nod = nod.next;
        }
        return nd;
    }
    public void Insert_Node(Node nd)
    {
        nd.next = null;
        nd.c_l = null;
        if (head == null)
        {
            head = nd;
            tail = nd;

        }
        else
        {
            tail.next = nd;
            tail = nd;
        }
    }
    public Node get_Nearest(Player_Loc loc)
    {
        Node strt = head;
        float d, min_dist = 100000.0f;
        Node nearest = null;
        while (strt != null)
        { 
            d = loc.getDist(strt);
            if (d < min_dist)
            {
                min_dist = d;
                nearest = strt;
            }
            strt = strt.next;
        }
        return nearest;
    }
    public C_List get_path_nodes(Node dst)
    {
        C_List lst = new C_List();
        Node nod = dst;
        while (nod != null)
        {
            lst.Add_node(nod);
            nod = nod.parent;
        }
        return lst;

    }
}