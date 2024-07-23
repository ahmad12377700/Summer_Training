using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player_Loc
{
    public float x, z;
    
    public Player_Loc(float xx, float zz)
    {
        x = xx; 
        z = zz;
    }

    public float getDist(Node nd)
    {
        float f = Mathf.Abs(x - nd.x) + Mathf.Abs(z - nd.z);
        return f;
    }
}
