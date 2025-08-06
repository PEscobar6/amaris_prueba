'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { TrendingUp, Plus, AlertCircle, CheckCircle } from 'lucide-react'
import { formatCurrency } from '@/lib/utils'
import { useToast } from '@/components/ui/use-toast'
import apiService from '@/services/api'
import type { Fund, Subscription } from '@/types'

interface FundsTabProps {
  funds: Fund[]
  subscriptions: Subscription[]
  onUpdate: () => void
}

export function FundsTab({ funds, subscriptions, onUpdate }: FundsTabProps) {
  const [selectedFund, setSelectedFund] = useState<Fund | null>(null)
  const [amount, setAmount] = useState('')
  const [notificationType, setNotificationType] = useState<'email' | 'sms'>('email')
  const [eligibility, setEligibility] = useState<any>(null)
  const [isSubscribing, setIsSubscribing] = useState(false)
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const { toast } = useToast()

  const subscribedFundIds = subscriptions.filter(s => s.is_active).map(s => s.fund_id)

  const handleFundSelect = async (fund: Fund) => {
    setSelectedFund(fund)
    setAmount(fund.minimum_amount.toString())
    setEligibility(null)
    setIsDialogOpen(true)
  }

  const checkEligibility = async () => {
    if (!selectedFund || !amount) return

    try {
      const result = await apiService.funds.checkEligibility(selectedFund.id, parseFloat(amount))
      setEligibility(result)
    } catch (error) {
      console.error('Error checking eligibility:', error)
      toast({
        title: "Error",
        description: "No se pudo verificar la elegibilidad",
        variant: "destructive",
      })
    }
  }

  const handleSubscription = async () => {
    if (!selectedFund || !amount || !eligibility?.eligible) return

    setIsSubscribing(true)
    try {
      await apiService.subscriptions.subscribe({
        fund_id: selectedFund.id,
        amount: parseFloat(amount),
        notification_type: notificationType,
      })

      toast({
        title: "¡Suscripción exitosa!",
        description: `Te has suscrito al fondo ${selectedFund.name}`,
      })

      setIsDialogOpen(false)
      onUpdate()
    } catch (error: any) {
      console.error('Error subscribing:', error)
      toast({
        title: "Error en la suscripción",
        description: error.response?.data?.detail || "No se pudo completar la suscripción",
        variant: "destructive",
      })
    } finally {
      setIsSubscribing(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Available Funds */}
      <div>
        <h3 className="text-lg font-semibold mb-4">Fondos Disponibles</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {funds.map((fund) => {
            const isSubscribed = subscribedFundIds.includes(fund.id)
            
            return (
              <Card key={fund.id} className={`cursor-pointer transition-all hover:shadow-md ${isSubscribed ? 'ring-2 ring-green-500' : ''}`}>
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-base">{fund.name}</CardTitle>
                    <Badge variant={fund.category === 'FPV' ? 'default' : 'secondary'}>
                      {fund.category}
                    </Badge>
                  </div>
                  <CardDescription className="text-sm">
                    Mínimo: {formatCurrency(fund.minimum_amount)}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {fund.description && (
                    <p className="text-sm text-muted-foreground mb-3">
                      {fund.description}
                    </p>
                  )}
                  
                  {isSubscribed ? (
                    <div className="flex items-center gap-2 text-green-600">
                      <CheckCircle className="h-4 w-4" />
                      <span className="text-sm font-medium">Ya suscrito</span>
                    </div>
                  ) : (
                    <Button 
                      onClick={() => handleFundSelect(fund)}
                      className="w-full"
                      size="sm"
                    >
                      <Plus className="h-4 w-4 mr-2" />
                      Suscribirse
                    </Button>
                  )}
                </CardContent>
              </Card>
            )
          })}
        </div>
      </div>

      {/* Active Subscriptions */}
      {subscriptions.filter(s => s.is_active).length > 0 && (
        <div>
          <h3 className="text-lg font-semibold mb-4">Mis Suscripciones</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {subscriptions.filter(s => s.is_active).map((subscription) => (
              <Card key={subscription.id}>
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-base">{subscription.fund_name}</CardTitle>
                    <Badge variant={subscription.fund_category === 'FPV' ? 'default' : 'secondary'}>
                      {subscription.fund_category}
                    </Badge>
                  </div>
                  <CardDescription>
                    Invertido: {formatCurrency(subscription.amount)}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <TrendingUp className="h-4 w-4" />
                    Suscrito el {new Date(subscription.subscribed_at).toLocaleDateString('es-CO')}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Subscription Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-[425px]">
          <DialogHeader>
            <DialogTitle>Suscribirse a {selectedFund?.name}</DialogTitle>
            <DialogDescription>
              Completa los datos para suscribirte a este fondo.
            </DialogDescription>
          </DialogHeader>
          
          <div className="grid gap-4 py-4">
            <div className="grid gap-2">
              <Label htmlFor="amount">Monto a invertir</Label>
              <Input
                id="amount"
                type="number"
                min={selectedFund?.minimum_amount}
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder={`Mínimo ${formatCurrency(selectedFund?.minimum_amount || 0)}`}
              />
              {selectedFund && (
                <p className="text-xs text-muted-foreground">
                  Monto mínimo: {formatCurrency(selectedFund.minimum_amount)}
                </p>
              )}
            </div>

            <div className="grid gap-2">
              <Label htmlFor="notification">Tipo de notificación</Label>
              <Select value={notificationType} onValueChange={(value: 'email' | 'sms') => setNotificationType(value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="email">Email</SelectItem>
                  <SelectItem value="sms">SMS</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <Button onClick={checkEligibility} variant="outline" className="w-full">
              Verificar Elegibilidad
            </Button>

            {eligibility && (
              <div className={`p-3 rounded-md border ${eligibility.eligible ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
                <div className="flex items-center gap-2">
                  {eligibility.eligible ? (
                    <CheckCircle className="h-4 w-4 text-green-600" />
                  ) : (
                    <AlertCircle className="h-4 w-4 text-red-600" />
                  )}
                  <p className={`text-sm ${eligibility.eligible ? 'text-green-800' : 'text-red-800'}`}>
                    {eligibility.message}
                  </p>
                </div>
                <div className="mt-2 text-xs text-muted-foreground">
                  <p>Saldo disponible: {formatCurrency(eligibility.user_balance)}</p>
                  <p>Monto requerido: {formatCurrency(eligibility.required_amount)}</p>
                </div>
              </div>
            )}
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setIsDialogOpen(false)}>
              Cancelar
            </Button>
            <Button 
              onClick={handleSubscription}
              disabled={!eligibility?.eligible || isSubscribing}
            >
              {isSubscribing ? 'Suscribiendo...' : 'Suscribirse'}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}