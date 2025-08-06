'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Settings, Mail, MessageSquare, User as UserIcon, Wallet } from 'lucide-react'
import { formatCurrency } from '@/lib/utils'
import { useToast } from '@/components/ui/use-toast'
import apiService from '@/services/api'
import type { User } from '@/types'

interface SettingsTabProps {
  user: User | null
  onUpdate: () => void
}

export function SettingsTab({ user, onUpdate }: SettingsTabProps) {
  const [notificationPreference, setNotificationPreference] = useState<'email' | 'sms'>(
    user?.notification_preference || 'email'
  )
  const [isUpdating, setIsUpdating] = useState(false)
  const { toast } = useToast()

  const handleUpdatePreference = async () => {
    if (!user || notificationPreference === user.notification_preference) return

    setIsUpdating(true)
    try {
      await apiService.user.updateNotificationPreference(notificationPreference)
      
      toast({
        title: "¡Configuración actualizada!",
        description: `Ahora recibirás notificaciones por ${notificationPreference === 'email' ? 'email' : 'SMS'}`,
      })

      onUpdate()
    } catch (error: any) {
      console.error('Error updating preference:', error)
      toast({
        title: "Error al actualizar",
        description: error.response?.data?.detail || "No se pudo actualizar la configuración",
        variant: "destructive",
      })
    } finally {
      setIsUpdating(false)
    }
  }

  if (!user) {
    return (
      <div className="flex items-center justify-center py-8">
        <p className="text-muted-foreground">Cargando configuración...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* User Profile Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
                            <UserIcon className="h-5 w-5" />
            Perfil de Usuario
          </CardTitle>
          <CardDescription>
            Información básica de tu cuenta
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <Label className="text-sm font-medium text-muted-foreground">
                Nombre completo
              </Label>
              <p className="mt-1 text-sm">{user.name}</p>
            </div>
            <div>
              <Label className="text-sm font-medium text-muted-foreground">
                Correo electrónico
              </Label>
              <p className="mt-1 text-sm">{user.email}</p>
            </div>
            <div>
              <Label className="text-sm font-medium text-muted-foreground">
                Teléfono
              </Label>
              <p className="mt-1 text-sm">{user.phone}</p>
            </div>
            <div>
              <Label className="text-sm font-medium text-muted-foreground">
                Miembro desde
              </Label>
              <p className="mt-1 text-sm">
                {new Date(user.created_at).toLocaleDateString('es-CO', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Balance Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Wallet className="h-5 w-5" />
            Información Financiera
          </CardTitle>
          <CardDescription>
            Estado actual de tu saldo
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-green-50 rounded-lg border border-green-200">
              <Label className="text-sm font-medium text-green-800">
                Saldo Disponible
              </Label>
              <p className="mt-1 text-2xl font-bold text-green-600">
                {formatCurrency(user.balance)}
              </p>
            </div>
            <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
              <Label className="text-sm font-medium text-blue-800">
                Estado de Cuenta
              </Label>
              <p className="mt-1 text-lg font-semibold text-blue-600">
                {user.is_active ? 'Activa' : 'Inactiva'}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Notification Preferences */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="h-5 w-5" />
            Preferencias de Notificación
          </CardTitle>
          <CardDescription>
            Configura cómo deseas recibir las notificaciones del sistema
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <Label htmlFor="notification-type">Método de notificación preferido</Label>
            <Select 
              value={notificationPreference} 
              onValueChange={(value: 'email' | 'sms') => setNotificationPreference(value)}
            >
              <SelectTrigger className="w-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="email">
                  <div className="flex items-center gap-2">
                    <Mail className="h-4 w-4" />
                    <span>Email ({user.email})</span>
                  </div>
                </SelectItem>
                <SelectItem value="sms">
                  <div className="flex items-center gap-2">
                    <MessageSquare className="h-4 w-4" />
                    <span>SMS ({user.phone})</span>
                  </div>
                </SelectItem>
              </SelectContent>
            </Select>
            
            <div className="text-sm text-muted-foreground">
              <p>Recibirás notificaciones para:</p>
              <ul className="mt-1 ml-4 space-y-1">
                <li>• Confirmaciones de suscripción a fondos</li>
                <li>• Confirmaciones de cancelación de suscripciones</li>
                <li>• Actualizaciones importantes del sistema</li>
              </ul>
            </div>
          </div>

          <div className="flex items-center justify-between pt-4 border-t">
            <div className="text-sm text-muted-foreground">
              Configuración actual: {user.notification_preference === 'email' ? 'Email' : 'SMS'}
            </div>
            <Button 
              onClick={handleUpdatePreference}
              disabled={isUpdating || notificationPreference === user.notification_preference}
            >
              {isUpdating ? 'Actualizando...' : 'Guardar Cambios'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* System Information */}
      <Card>
        <CardHeader>
          <CardTitle>Información del Sistema</CardTitle>
          <CardDescription>
            Detalles técnicos y de soporte
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <Label className="font-medium text-muted-foreground">
                Versión del Sistema
              </Label>
              <p>FPV Management v1.0.0</p>
            </div>
            <div>
              <Label className="font-medium text-muted-foreground">
                Última Actualización
              </Label>
              <p>{new Date(user.updated_at).toLocaleDateString('es-CO')}</p>
            </div>
            <div>
              <Label className="font-medium text-muted-foreground">
                ID de Usuario
              </Label>
              <p className="font-mono">#{user.id.toString().padStart(6, '0')}</p>
            </div>
            <div>
              <Label className="font-medium text-muted-foreground">
                Soporte Técnico
              </Label>
              <p>soporte@fpv-system.com</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}