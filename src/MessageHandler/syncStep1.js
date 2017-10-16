import BinaryEncoder from '../Binary/Encoder.js'
import { readStateSet, writeStateSet } from './stateSet.js'
import { writeDeleteSet } from './deleteSet.js'
import ID from '../Util/ID.js'

export function stringifySyncStep1 (decoder, strBuilder) {
  let auth = decoder.readVarString()
  let protocolVersion = decoder.readVarUint()
  strBuilder.push(`
  - auth: "${auth}"
  - protocolVersion: ${protocolVersion}
`)
  // write SS
  strBuilder.push('  == SS: \n')
  let len = decoder.readUint32()
  for (let i = 0; i < len; i++) {
    let user = decoder.readVarUint()
    let clock = decoder.readVarUint()
    strBuilder.push(`     ${user}: ${clock}\n`)
  }
}

export function sendSyncStep1 (connector, syncUser) {
  let encoder = new BinaryEncoder()
  encoder.writeVarString(connector.y.room)
  encoder.writeVarString('sync step 1')
  encoder.writeVarString(connector.authInfo || '')
  encoder.writeVarUint(connector.protocolVersion)
  writeStateSet(connector.y, encoder)
  connector.send(syncUser, encoder.createBuffer())
}

export default function writeStructs (encoder, decoder, y, ss) {
  for (let [user, clock] of ss) {
    y.os.iterate(new ID(user, clock), null, function (struct) {
      struct._toBinary(encoder)
    })
  }
}

export function readSyncStep1 (decoder, encoder, y, senderConn, sender) {
  let protocolVersion = decoder.readVarUint()
  // check protocol version
  if (protocolVersion !== y.connector.protocolVersion) {
    console.warn(
      `You tried to sync with a Yjs instance that has a different protocol version
      (You: ${protocolVersion}, Client: ${protocolVersion}).
      `)
    y.destroy()
  }
  // write sync step 2
  encoder.writeVarString('sync step 2')
  encoder.writeVarString(y.connector.authInfo || '')
  writeDeleteSet(y, encoder)
  const ss = readStateSet(decoder)
  writeStructs(encoder, decoder, y, ss)
  y.connector.send(senderConn.uid, encoder.createBuffer())
  senderConn.receivedSyncStep2 = true
  if (y.connector.role === 'slave') {
    sendSyncStep1(y.connector, sender)
  }
}