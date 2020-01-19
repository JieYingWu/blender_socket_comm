# Author: Adnan Munawar
# Email: amunawa2@jh.edu
# Lab: LCSR

bl_info = {
    "name": "Socket Client for Blender",
    "author": "Adnan Munawar",
    "version": (0, 1),
    "blender": (2, 79, 0),
    "location": "View3D > Tool > SocketClient",
    "description": "",
    "warning": "",
    "wiki_url": "https://github.com/adnanmunawar/blender_socket_comm",
    "category": "SocketClient",
}

import bpy
from bpy.props import StringProperty, IntProperty
import socket
from collections import Counter

# Globals
server_addr = ''
server_port = 3004
client = None


def connect(addr=None, port=None):
    global server_addr, server_port, client
    if addr is not None:
        server_addr = addr
    if port is not None:
        server_port = port

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_addr, server_port))
    client.setblocking(False)


def disconnect():
    print('Disconnect Called')
    if client:
        print('Closing Client', client)
        client.close()


def client_rx(args):
    try:
        packet = client.recv(1024)
        packet = packet.decode()
        try:
            idx, x, y, z = packet.split(',')
            idx = int(idx)
            x = float(x)
            y = float(y)
            z = float(z)
            # print('MOVING VTX(', idx, ') : ', x, y, z)
            if bpy.context.object:
                bpy.context.object.data.vertices[idx].co = (x,y,z)
        except ValueError:
            pass
    except socket.error:
        pass


class ConnectOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "scene.socket_connect_operator"
    bl_label = "Connect Operator"

    def execute(self, context):
        if client is None:
            connect(context.scene.server_addr, context.scene.server_port)
            bpy.app.handlers.scene_update_pre.append(client_rx)
        return {'FINISHED'}


class DisconnectOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "scene.socket_disconnect_operator"
    bl_label = "Disconnect Operator"

    def execute(self, context):
        disconnect()
        return {'FINISHED'}


class BlenderClientPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Blender Client Panel"
    bl_idname = "Blender_PT_Client"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "SocketClient"

    bpy.types.Scene.server_addr = StringProperty(name="Server Addr", default="localhost", description="Server Addr")
    bpy.types.Scene.server_port = IntProperty(name="Server Port", default=3001, description="Server Port")

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Blender Client!", icon='WORLD_DATA')

        row = layout.row()
        row.prop(context.scene, 'server_addr')

        row = layout.row()
        row.prop(context.scene, 'server_port')

        row = layout.row()
        row.operator('scene.socket_connect_operator')

        row = layout.row()
        row.operator('scene.socket_disconnect_operator')


classes = (ConnectOperator, DisconnectOperator, BlenderClientPanel)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
    #ungregister()
